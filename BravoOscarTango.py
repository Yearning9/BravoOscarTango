import discord
import os
import json
from discord.ext import commands
from discord.ext.commands import NotOwner
from discord.ext.commands import CommandNotFound
from discord.ext.commands import MissingPermissions
from discord.ext.commands import MissingRequiredArgument

# dictionary of afk users
afkdict = {}


def get_prefix(client, message):
    with open('Private/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)

# remove default help command because I don't like it
client.remove_command("help")


def guild_id(ctx):
    with open('Private/DiscordServer.txt', 'r')as f:
        discord_id = int(f.read())
    return ctx.guild.id == discord_id


with open('Private/Discord.txt', 'r') as g:
    token: str = g.read()

prfx = '.'

@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.competing, name='flight simming (.commands)'))
    print('Bot is ready')


@client.event
async def on_guild_join(guild):
    with open('Private/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('Private/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('Private/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('Private/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command(aliases=['changeprefix'])
@commands.has_permissions(administrator=True)
async def prefix(ctx, new_prefix):
    if len(new_prefix) > 2:
        ctx.reply("Please use a max of 2 characters")
        return

    with open('Private/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = new_prefix

    with open('Private/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.reply(f'Bot prefix set to: {new_prefix}', mention_author=False)


@client.command()
@commands.is_owner()
async def test(ctx):
    await ctx.send(f'Startup check succesful, check console for ping, commands on {prfx}commands')
    print(f'{round(client.latency * 1000)} ms')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f'Command does not exist, check {prfx}commands or {prfx}modcommands for a list of commands')


@test.error
async def test_error(ctx, error):
    if isinstance(error, NotOwner):
        await ctx.send("This command is only intended for use by owner")


@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('You have to be a server admin to change the prefix')
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please specify a prefix')


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

@client.command()
async def invite(ctx):
    await ctx.reply('Invite for BravoOscarTango: https://discord.com/oauth2/authorize?client_id=728998963054903388&permissions=280291398&scope=bot')

@client.event
async def on_message(message):
    global afkdict
    user = client.get_user(message.author.id)
    if message.content == "balls 🗿" or message.content == "Balls 🗿":
        await message.channel.send("<:sad:776437812865007616>")
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
