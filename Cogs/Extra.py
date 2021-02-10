import discord
from discord.ext import commands
# from WonderfulBot import guild_prefix

prfx = '.'

class Extra(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['commands'])
    async def help(self, ctx):
        embed = discord.Embed(
            title='***List of commands***',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_footer(text=f'To see other commands use {prfx}commands')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed.add_field(name=f'{prfx}flightcommands :airplane_departure:', value='List of flight sim commands', inline=False),
        embed.add_field(name=f'{prfx}music :cd:', value='List of music commands', inline=False)
        embed.add_field(name=f'{prfx}modcommands :tools:', value='List of mod commands, all require special permissions',
                        inline=False)
        embed.add_field(name=f'{prfx}funcommands :beach_umbrella:', value='List of fun commands', inline=False),
        embed.add_field(name=f'{prfx}extracommands :unlock:', value='List of extra commands', inline=False),
        embed.add_field(name=f'{prfx}invite :incoming_envelope:', value='Bot invite', inline=False)


        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def funcommands(self, ctx):
        embed = discord.Embed(
            title='***List of commands***',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_footer(text=f'To see other commands use {prfx}commands')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        # embed.add_field(name=f'{prfx}vuling', value='To pray for our eternal god', inline=False)
        # embed.add_field(name=f'{prfx}colonialism', value='Very unbiased command', inline=False)
        # embed.add_field(name=f'{prfx}md11', value='Another very unbiased command', inline=False)
        embed.add_field(name=f'{prfx}zalgo ({prfx}z)', value='Translates text to zalgo, not effective for long sentences', inline=False)
        embed.add_field(name=f'{prfx}markov ({prfx}mk)', value='Generates a sentence based on a txt file, in this case the Communist Manifesto :)', inline=False)
        embed.add_field(name=f'{prfx}garloc',
                        value='Õ̷̗h̶̰̀ ̶̭̋m̷̥͌a̶̺͂n̷͓̊ ̵̫̒p̴̹͐ḻ̸̑s̷͈̋ ̷͍̾h̵̹̓e̴̻̽l̵̈́͜p̸̝̽ ̴̗̄w̷͇̐ĩ̸͇t̸͖̐h̸̗̀ ̴̜̀c̵̤̾o̷̢̚ṃ̴͝p̶̜̓u̵͜͠t̷̓͜e̷̗͆ŕ̶̩',
                        inline=False)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def modcommands(self, ctx):
        embed = discord.Embed(
            title='List of mod commands',
            description='All of these need mod/admin permissions',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_footer(text=f'To see other commands use {prfx}commands')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed.add_field(name=f'{prfx}test', value='Startup check', inline=False)
        embed.add_field(name=f'{prfx}clear [amount]', value='Clears messages, 1 by default', inline=False)
        embed.add_field(name=f'{prfx}ban [member][reason]', value='To ban a member, default reason is None', inline=False)
        embed.add_field(name=f'{prfx}kick [member][reason]', value='To kick a member, default reason is None', inline=False)
        embed.add_field(name=f'{prfx}mute [member][reason]', value='To mute a member, default reason is None', inline=False)
        embed.add_field(name=f'{prfx}unmute [member]', value='To unmute a muted member', inline=False)
        embed.add_field(name=f'{prfx}changeprefix [prefix]', value="Change the bot's prefix", inline=False)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def music(self, ctx):
        embed = discord.Embed(
            title='***List of music commands***',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed.add_field(name=f'{prfx}join ({prfx}j)', value='Makes bot join same voice channel you are in', inline=False)
        embed.add_field(name=f'{prfx}leave ({prfx}l)', value='Makes bot leave voice channel', inline=False)
        embed.add_field(name=f'{prfx}play ({prfx}p) [url/song title]',
                        value='Plays song either from url or searches for closest match', inline=False)
        embed.add_field(name=f'{prfx}lyrics ({prfx}ly) [Search query]', value='[Genius] Searches for lyrics for given query, or for the current song if none is specified', inline=False)
        embed.add_field(name=f'{prfx}pause ({prfx}pp)', value='Pauses music', inline=False)
        embed.add_field(name=f'{prfx}resume ({prfx}r)', value='Resumes paused music', inline=False)
        embed.add_field(name=f'{prfx}np', value='Shows song that is currently playing', inline=False)
        embed.add_field(name=f'{prfx}stop', value='Stops music and clears queue', inline=False)
        embed.add_field(name=f'{prfx}skip', value='Skip to next song in queue', inline=False)
        embed.add_field(name=f'{prfx}queue', value='Shows the current queue', inline=False)
        embed.add_field(name=f'{prfx}shuffle', value='Shuffles current queue', inline=False)
        embed.add_field(name=f'{prfx}remove [song queue number]', value='Searches for song in queue and removes it',
                        inline=False)
        embed.add_field(name=f'{prfx}loop', value='Loops current song, use again to unloop', inline=False),
        embed.set_footer(text="Adapted from vbe0201's music bot")

        await ctx.reply(embed=embed, mention_author=False)


    @commands.command()
    async def flightcommands(self, ctx):
        embed = discord.Embed(
            title='List of flight sim commands',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_footer(text=f'To see other commands use {prfx}commands')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed.add_field(name=f'{prfx}metar ({prfx}wx) [ICAO]', value='Fetches METAR for given airport ICAO', inline=False)
        embed.add_field(name=f'{prfx}charts ({prfx}ch) [ICAO]', value='Returns PDF chart for given airport ICAO', inline=False)
        embed.add_field(name=f'{prfx}checklist ({prfx}cl) [Aircraft ICAO]', value='Returns checklist for supported aircraft ICAO', inline=False)
        embed.add_field(name=f'{prfx}flightplan ({prfx}fl) [Departure ICAO][Arrival ICAO]', value='Calculates a flight plan between two given airports', inline=False)
        embed.add_field(name=f'{prfx}download [File format]', value='Returns link to download FMS plan in the given format', inline=False)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def extracommands(self, ctx):
        embed = discord.Embed(
            title='List of extra commands',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_footer(text=f'To see other commands use {prfx}commands')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed.add_field(name=f'{prfx}covid [Country]',
                        value='Shows Covid19 stats for a given country, or country with most cases if none is specified',
                        inline=False)
        embed.add_field(name=f'{prfx}gif ({prfx}g) [GIF search query]',
                        value='[Tenor] Searches and posts a GIF based on the given query', inline=False)
        embed.add_field(name=f'{prfx}afk',
                        value="You'll be set as AFK, if someone tags you while AFK they'll be notified about it. Use again or send a message to remove AFK status",
                        inline=False)
        embed.add_field(name=f'{prfx}pic [Image search query]',
                        value="[Google Images] Searches and posts a picture based on the given query", inline=False)
        await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(Extra(client))
