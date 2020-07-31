import discord
from discord.ext import commands


class Extra(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['commands'])
    async def help(self, ctx):
        embed = discord.Embed(
            title='***List of commands***',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_footer(text='Remember to pray to Vuling')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed.add_field(name='.flight (.ff) {IATA callsign}',
                        value='Shows info on an active flight or a list of scheduled/past flights', inline=False)
        embed.add_field(name='.covid {Country}',
                        value='Shows Covid19 stats for a given country, or country with most cases if none is specified',
                        inline=False)
        embed.add_field(name='.gif (.g) {GIF search query}',
                        value='[Tenor] Searches and posts a GIF based on the given query', inline=False)
        embed.add_field(name='.afk',
                        value="You'll be set as AFK, if someone tags you while AFK they'll be notified about it. Use again or send a message to remove AFK",
                        inline=False)
        embed.add_field(name='.pic {Image search query}',
                        value="[Google Images] Searches and posts a picture based on the given query", inline=False)
        embed.add_field(name='.vuling', value='To pray for our eternal god', inline=False)
        embed.add_field(name='.colonialism', value='Very unbiased command', inline=False)
        embed.add_field(name='.md11', value='Another very unbiased command', inline=False)
        embed.add_field(name='.garloc',
                        value='Õ̷̗h̶̰̀ ̶̭̋m̷̥͌a̶̺͂n̷͓̊ ̵̫̒p̴̹͐ḻ̸̑s̷͈̋ ̷͍̾h̵̹̓e̴̻̽l̵̈́͜p̸̝̽ ̴̗̄w̷͇̐ĩ̸͇t̸͖̐h̸̗̀ ̴̜̀c̵̤̾o̷̢̚ṃ̴͝p̶̜̓u̵͜͠t̷̓͜e̷̗͆ŕ̶̩',
                        inline=False)
        embed.add_field(name='.music', value='List of music commands', inline=False)
        embed.add_field(name='.modcommands', value='List of mod commands, all require special permissions',
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def modcommands(self, ctx):
        embed = discord.Embed(
            title='List of mod commands',
            description='All of these need mod permissions',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_footer(text='Remember to pray to Vuling')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed.add_field(name='.test', value='Startup check', inline=False)
        embed.add_field(name='.clear {amount}', value='Clears messages, 1 by default', inline=False)
        embed.add_field(name='.ban {member}{reason}', value='To ban a member, default reason is None', inline=False)
        embed.add_field(name='.kick {member}{reason}', value='To kick a member, default reason is None', inline=False)
        embed.add_field(name='.mute {member}{reason}', value='To mute a member, default reason is None', inline=False)
        embed.add_field(name='.unmute {member}', value='To unmute a muted member', inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def music(self, ctx):
        embed = discord.Embed(
            title='***List of music commands (Just testing for now)***',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed.add_field(name='.join (.j)', value='Makes bot join same voice channel you are in', inline=False)
        embed.add_field(name='.leave (.l)', value='Makes bot leave voice channel', inline=False)
        embed.add_field(name='.play (.p) {url/song title}',
                        value='Plays song either from url or searches for closest match', inline=False)
        embed.add_field(name='.lyrics (.ly)', value='[Genius] Searches for lyrics for the current song', inline=False)
        embed.add_field(name='.pause (.pp)', value='Pauses music', inline=False)
        embed.add_field(name='.resume (.r)', value='Resumes paused music', inline=False)
        embed.add_field(name='.np', value='Shows song that is currently playing', inline=False)
        embed.add_field(name='.stop', value='Stops music and clears queue', inline=False)
        embed.add_field(name='.skip', value='Skip to next song in queue', inline=False)
        embed.add_field(name='.queue', value='Shows the current queue', inline=False)
        embed.add_field(name='.shuffle', value='Shuffles current queue', inline=False)
        embed.add_field(name='.remove {song queue number}', value='Searches for song in queue and removes it',
                        inline=False)
        embed.add_field(name='.loop', value='Loops current song, use again to unloop', inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Extra(client))
