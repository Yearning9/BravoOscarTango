import discord
from discord.ext import commands
from BravoOscarTango import get_prefix


class Extra(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['commands'])
    async def help(self, ctx):
        prfx = get_prefix(client=self, message=ctx.message)
        embed = discord.Embed(
            title='***List of commands***',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed.add_field(name=f'{prfx}flightcommands :airplane_departure:', value='List of flight sim commands', inline=False),
        embed.add_field(name=f'{prfx}music :cd:', value='List of music commands', inline=False)
        embed.add_field(name=f'{prfx}modcommands :tools:', value='List of mod commands, all require special permissions',
                        inline=False)
        embed.add_field(name=f'{prfx}funcommands :beach_umbrella:', value='List of fun commands', inline=False),
        embed.add_field(name=f'{prfx}extracommands :unlock:', value='List of extra commands', inline=False),
        embed.add_field(name=f'{prfx}invite :incoming_envelope:', value='Bot invite', inline=False)
        embed.add_field(name=f'{prfx}feedback/{prfx}support :card_box:', value='Provide feedback or ask for support', inline=False)
        embed.add_field(name=f'{prfx}donate :heart:', value='Donate to the bot', inline=False)


        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def funcommands(self, ctx):
        prfx = get_prefix(client=self, message=ctx.message)
        embed = discord.Embed(
            title='***List of commands***',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_footer(text=f'To see other commands use {prfx}commands')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed.add_field(name=f'{prfx}zalgo ({prfx}z)', value='Translates text to zalgo, not effective for long sentences', inline=False)
        embed.add_field(name=f'{prfx}markov ({prfx}mk)', value='Generates a sentence based on the Communist Manifesto :)', inline=False)
        embed.add_field(name=f'{prfx}garloc',
                        value='Õ̷̗h̶̰̀ ̶̭̋m̷̥͌a̶̺͂n̷͓̊ ̵̫̒p̴̹͐ḻ̸̑s̷͈̋ ̷͍̾h̵̹̓e̴̻̽l̵̈́͜p̸̝̽ ̴̗̄w̷͇̐ĩ̸͇t̸͖̐h̸̗̀ ̴̜̀c̵̤̾o̷̢̚ṃ̴͝p̶̜̓u̵͜͠t̷̓͜e̷̗͆ŕ̶̩',
                        inline=False)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def modcommands(self, ctx):
        prfx = get_prefix(client=self, message=ctx.message)
        embed = discord.Embed(
            title='List of mod commands',
            description='All of these need mod permissions',
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
        embed.add_field(name=f'{prfx}changeprefix [new prefix]', value='To change the bot prefix', inline=False)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def music(self, ctx):
        prfx = get_prefix(client=self, message=ctx.message)
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
        prfx = get_prefix(client=self, message=ctx.message)
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
        embed.add_field(name=f'{prfx}simbrief ({prfx}sb) [Username]', value='Returns your last flight plan generated with SimBrief (WILL NOT GENERATE A FLIGHT PLAN, can be used in a private chat if you prefer to keep the username hidden)', inline=False)
        embed.add_field(name=f'{prfx}info [ICAO]', value='Shows various info about a given airport ICAO', inline=False)
        embed.add_field(name=f'{prfx}notam [ICAO] [Page]', value='Shows a list of NOTAMs for given airport ICAO, page number is optional', inline=False)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def extracommands(self, ctx):
        prfx = get_prefix(client=self, message=ctx.message)
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
        embed.add_field(name=f'{prfx}pic [Image search query]',
                        value="[Bing Images] Searches and posts a picture based on the given query", inline=False)
        await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(Extra(client))
