import discord
import os
from discord.ext import commands
from discord.ext.commands import NotOwner
from discord.ext.commands import CommandNotFound


# prefix
client = commands.Bot(command_prefix='.')

# dictionary of afk users
afkdict = {}

# remove default help command because I don't like it
client.remove_command("help")

def guild_id(ctx):
    with open('Private/DiscordServer.txt', 'r')as f:
        discord_id = int(f.read())
    return ctx.guild.id == discord_id


with open('Private/Discord.txt', 'r') as g:
    token: str = g.read()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('instead of studying (.commands)'))
    print('Bot is ready')


@client.command()
@commands.is_owner()
async def test(ctx):
    await ctx.send('Startup check succesful, check console for ping, commands on .commands')
    print(f'{round(client.latency * 1000)} ms')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('Command does not exist, check .commands or .modcommands for a list of commands')


@test.error
async def test_error(ctx, error):
    if isinstance(error, NotOwner):
        await ctx.send("This command is only intended for use by owner")


@client.command()
async def afk(ctx):
    global afkdict
    user = client.get_user(ctx.message.author.id)
    if ctx.message.author in afkdict:
        afkdict.pop(ctx.message.author)
        await ctx.channel.purge(limit=1)
        await user.send('You are no longer AFK')
    else:
        afkdict[ctx.message.author] = ctx.message.author.id
        await ctx.channel.purge(limit=1)
        await user.send(f"You are now AFK in {ctx.guild}")


@client.event
async def on_message(message):
    global afkdict
    user = client.get_user(message.author.id)
    if message.author in afkdict:
        afkdict.pop(message.author)
        await user.send('You are no longer AFK')
    for member in message.mentions:
        if member != message.author:
            if member in afkdict:
                await user.send(f"{member} is AFK")
    await client.process_commands(message)



for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')


client.run(token)
