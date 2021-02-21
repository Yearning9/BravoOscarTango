import discord
import os
from discord.ext import commands
from discord.ext.commands import NotOwner, CommandNotFound
from Cogs.Prefixes import db, PrefixDatabase
from discord_slash import SlashCommand, manage_commands

# dictionary of afk users
# afkdict = {}


def get_prefix(client, message):
    try:
        guild_prefix = db.session.query(PrefixDatabase).filter_by(id_guild=str(message.guild.id)).first()
        return str(guild_prefix.prefix)
    except AttributeError:
        prefix = '.'
        data = PrefixDatabase(str(message.guild.id), prefix)
        db.session.add(data)
        db.session.commit()
        print(f'Added {str(message.guild.id)}')
        return '.'


client = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
# client = commands.Bot(command_prefix='.')  # let's call this an emergency measure for prefixes

# remove default help command because I don't like it
client.remove_command("help")

slash = SlashCommand(client, sync_commands=True, override_type=True)

def guild_id(ctx):
    with open('Private/DiscordServer.txt', 'r')as f:
        discord_id = int(f.read())
    return ctx.guild.id == discord_id


with open('Private/Discord.txt', 'r') as g:
    token: str = g.read()


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.competing, name='flight simming (.commands)'))
    print('Bot is ready')


@client.event
async def on_guild_join(guild):
    if db.session.query(PrefixDatabase).filter(PrefixDatabase.id_guild == str(guild.id)).count() == 0:
        prefix = '.'
        data = PrefixDatabase(str(guild.id), prefix)
        db.session.add(data)
        db.session.commit()
        print(f'Added {str(guild.id)}')
    else:
        guild_db = db.session.query(PrefixDatabase).filter_by(id_guild=str(guild.id)).first()
        guild_db.prefix = '.'
        db.session.commit()


@client.command()
@commands.is_owner()
async def test(ctx):
    prfx = get_prefix(client, message=ctx.message)
    await ctx.send(f'Startup check succesful, check console for ping, commands on {prfx}commands')
    print(f'{round(client.latency * 1000)} ms')


@client.event
async def on_command_error(ctx, error):
    prfx = get_prefix(client, message=ctx.message)
    if isinstance(error, CommandNotFound):
        await ctx.send(f'Command does not exist, check {prfx}commands or {prfx}modcommands for a list of commands')


@test.error
async def test_error(ctx, error):
    if isinstance(error, NotOwner):
        await ctx.send("This command is only intended for use by owner")


# @client.command()
# async def afk(ctx):
#     global afkdict
#     user = client.get_user(ctx.message.author.id)
#     if ctx.message.author in afkdict:
#         afkdict.pop(ctx.message.author)
#         await ctx.channel.purge(limit=1)
#         await user.send('You are no longer AFK')
#     else:
#         afkdict[ctx.message.author] = ctx.message.author.id
#         await ctx.channel.purge(limit=1)
#         await user.send(f"You are now AFK in {ctx.guild}")


@client.command()
async def invite(ctx):
    await ctx.reply(
        'Invite for BravoOscarTango: https://discord.com/api/oauth2/authorize?client_id=728998963054903388&permissions=271902726&scope=bot')


@client.event
async def on_message(message):
    global afkdict
    user = client.get_user(message.author.id)
    if message.content == "balls 🗿" or message.content == "Balls 🗿":
        await message.channel.send("<:sad:776437812865007616>")
    # if message.author in afkdict:
    #     afkdict.pop(message.author)
    #     await user.send('You are no longer AFK')
    # for member in message.mentions:
    #     if member != message.author:
    #         if member in afkdict:
    #             await user.send(f"{member} is AFK")

    await client.process_commands(message)


@client.command(aliases=['fb'])
async def feedback(ctx):
    await ctx.reply(
        'Thank you for wanting to provide feedback! Please fill in the short form at https://bravooscartangofb.herokuapp.com',
        mention_author=False)


for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')

client.run(token)
