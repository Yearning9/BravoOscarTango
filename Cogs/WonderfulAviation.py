import discord
from discord.ext import commands
from discord.ext.commands import check
from WonderfulBot import guild_id


class Avia(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['a'])
    @check(guild_id)
    async def aircraft(self, ctx):
        embed4 = discord.Embed(
            title='List of current available aircraft',
            description='Please report broken/missing links',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed4.set_footer(text='Page 1/3, use .a2 for page 2, .a3 for page 3')
        embed4.set_thumbnail(url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed4.add_field(name='Felis TY-154',
                         value='[Mega](https://mega.nz/#!kXgB2JCA!_G7A2AwznZl3ZF_6l1h8O_dbha323cfl86oTGoRYtP8) || [2.0.5 Update](https://drive.google.com/drive/u/0/folders/1x0fqCgNwcAiETf5AxVHYP8TogNgPMf4E)')
        embed4.add_field(name='IXEG 733',
                         value='[Mega](https://mega.nz/#!TZ0hGSiC!5gybC4qL1qZMfW0kCs_7cgFgquqKboqy4mOtm27El0w)')
        embed4.add_field(name='Dden Challenger',
                         value='[Mega](https://mega.nz/#!2c9HhawK!w45klJJHRw-4Byd-e0gd_WOWo2wBqOYPen9wv7cF3p4)')
        embed4.add_field(name='Toliss A319 v1.4', value='[Modsfire](https://modsfire.com/R0Qw0PL23D1GcyW)')
        embed4.add_field(name='VSL P2006T', value='[Mega](https://mega.nz/#F!nRsHiY6Q!X-ulDI1afAfug37Ux37d-A)')
        embed4.add_field(name='FF757 2.3.9',
                         value='[Mega](https://mega.nz/#!lCAywCjA!JMpItb_u-IkpP6XqPpS19CGNuzv_W3JjAPbMWSGXdWw)')
        embed4.add_field(name='FF A350 1.4.6',
                         value='[Mega](https://mega.nz/#!7FEQnSyZ!wc22u5wuIPRVYtcxnpB1gZ-E2k4W9-aB-0Q0c7-wqt8)')
        embed4.add_field(name='Colimata Concorde',
                         value='[Mega 1.10](https://mega.nz/#F!HQllQCbb!qUiUBz6M9Lorx3gibD_AAQ) || [Updates](https://forums.x-plane.org/index.php?/forums/forum/477-concorde-fxp/)')
        embed4.add_field(name='WW 737 MAX7/8/9/10 and 737-600',
                         value='[Website](http://www.maxteamdesign.com/download/)')
        embed4.add_field(name='TY204',
                         value='[Mega](https://mega.nz/#!Fd50GI5R!9qOzhy0Zqea0p0Te37-Z9SfaUny4MJ3cHMaHKBfdIt0)')
        embed4.add_field(name='Toliss A321/Magknight 787/Wilson Aircraft/FJS 727 + a lot more',
                         value='[Rutracker](https://rutracker.org/forum/viewtopic.php?t=5498752&start=390)')
        embed4.add_field(name='SSG 748 v1.91',
                         value='[Mega](https://mega.nz/file/KJszzbAa#AvJDXL_BAPb2ycGF95xgoA-2UpZnMEUvYl4PlqMXYXQ)')

        embed5 = discord.Embed(
            title='List of current available aircraft',
            description='Please report broken/missing links',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed5.set_footer(text='Page 2/3, use .a1 for page 1, .a3 for page 3')
        embed5.set_thumbnail(url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed5.add_field(name='FF 767 1.3.3', value='[Modsfire](https://modsfire.com/71zFZ3FkHCWOVos)')
        embed5.add_field(name='A400',
                         value='[Rutracker](https://rutracker.org/forum/out.php?url=https%3A%2F%2Fmodsfire.com%2Flm64T3yUHtKwL5X&p=79130554&t=5498752&f=2012&u=22310363)')
        embed5.add_field(name='Rotate MD-80 1.42r4',
                         value='[Mega](https://mega.nz/#!bc0mFQrB!MRs8t77J6RSokiKY3pfF0nHRQiCA0fP8IBHas_DvvMk)')
        embed5.add_field(name='Carenado PC12 1.3',
                         value='[Mega](https://mega.nz/#!nFlSTIQa!kbsV-FdaHxmjAxt-uuQY2XqPlaU5zwRCSTFQc-e04Y0)')
        embed5.add_field(name='VFlyteAir C150',
                         value='[Mega](https://mega.nz/#!DJkCkIwZ!ml2gWj2VsmmGiErwCenEn4V6RRnYM2OLmyKR1yK1Jug)')
        embed5.add_field(name='FF 777',
                         value='[Mega](https://mega.nz/#!GE1hjYqI!qhFHvHIH0CKP6KGEB-6__j4--aS2bFdFJwEEvNi0in4)')
        embed5.add_field(name='JAR A320',
                         value='[Mega](https://mega.nz/#!7E9jDIgZ!AirC-J_Qvb3U9AH0p8eBz2L2xDEpTavKg49PhmCzmeg)')
        embed5.add_field(name='FJS 737-200',
                         value='[Mega](https://mega.nz/file/SJNRUSAa#XeDiqnDWuTIlHjXmspJIk6Vd4IQlyo4QYedOoxQW_no)')
        embed5.add_field(name='Quest Kodiak',
                         value='[Mega](https://mega.nz/#!3VVQiIAZ!JvQlwaEaZAMUwa5cz9qGGPaLNUG4CPS417Nmkjdt3Dk)')
        embed5.add_field(name='FSLabs ConcordeX [P3D V3]',
                         value='[Mega](https://mega.nz/#!OQF3HQwS!nzlVjWkxnYOZhWeXRaB1wxZjZzT83VtMnr5KkoIGy2U)')
        embed5.add_field(name='AOA V-22 Osprey 1.7',
                         value='[yggtorrent](https://www2.yggtorrent.se/torrent/jeu-vid%C3%A9o/windows/587596-x-plane+aoa+simulation+v-22b+osprey+v1+7+pour+x-plane+11)')

        embed6 = discord.Embed(
            title='List of current available aircraft',
            description='Please report broken/missing links',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed6.set_footer(text='Page 3/3, use .a1 for page 1, .a2 for page 2')
        embed6.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed6.add_field(name='X-Craft ERJ Series [Rough crack]',
                         value='[Mega](https://mega.nz/#!jB1XkBZC!WTAoiT_zneFw4ttE3A-7hnCt3je8q6snRA6oS_nhpm8)')
        embed6.add_field(name='Carenado 390 Premier',
                         value='[Mediafire](https://www.mediafire.com/file/o5vxg80iwk0ixrn/Carenado_390_Premier_IA_v1.2.7z/file)')
        embed6.add_field(name='JU52',
                         value='[Mega](https://mega.nz/file/nwdXzQaT#TFOOZKM9jqCHzvXcWW6XchiDVrCeG6odfBIVexyA71M)')
        embed6.add_field(name='X-Trident Tornado',
                         value='[Mediafire](https://www.mediafire.com/file/88pbpctk1pp5t6b/banana.zip/file)')

        await ctx.send(embed=embed4)

        @commands.command()
        async def a1(ctx):
            await ctx.channel.purge(limit=2)
            await ctx.send(embed=embed4)

        @commands.command()
        async def a2(ctx):
            await ctx.channel.purge(limit=2)
            await ctx.send(embed=embed5)

        @commands.command()
        async def a3(ctx):
            await ctx.channel.purge(limit=2)
            await ctx.send(embed=embed6)

    @commands.command(aliases=['conv', 'c'])
    @check(guild_id)
    async def conversions(self, ctx):
        embed1 = discord.Embed(
            title='List of current available conversions',
            description='Please report broken/missing links, most of these are by Squawk7700 and require [SAM](https://forum.thresholdx.net/files/file/122-sam-scenery-animation-manager/)',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed1.set_footer(text='Page 1/3, use .c2 for page 2, .c3 for page 3')
        embed1.set_thumbnail(url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed1.add_field(name='DTTJ',
                         value='[Mega](https://mega.nz/#!qB1i2A6C!vtjr-6UmikZ_HkpMfPeKORmYk9D6IogClhQTEpUjF90)')
        embed1.add_field(name='EGKK',
                         value='[Mega](https://mega.nz/#!nFtwmAzC!oQx9rAjM5fWUvDH0hiwSKjHxr95-rgYZs5qcFl9BtSg)')
        embed1.add_field(name='FIMP',
                         value='[Mega](https://mega.nz/#!rR8mGQaL!qch2-JBbcfzw1Sq4y_pusn4uRFuf3dyr4TfFsgfzMeI)')
        embed1.add_field(name='FMEE',
                         value='[Mega](https://mega.nz/#!HN1CnShJ!xYZwoUbM0XHtyIvgX5254b3KDyyaIJRcIY2ee0IxTTA)')
        embed1.add_field(name='GMMX',
                         value='[Mega](https://mega.nz/#!DJ9iXC5b!mj3pFO4CA2afkArZdinEAsKlJKiOz84Fo2DpGDxvzWs) || Requires [Hard_Surface Library](https://forums.x-plane.org/index.php?/files/file/13129-hard-surface-library/)')
        embed1.add_field(name='KEGE',
                         value='[Mega](https://mega.nz/#!aE9QSAxL!7Xtq92RxemOD-QTBahDXzCm0eIjj8pIlk7W31ie6cQ0)')
        embed1.add_field(name='LEST', value='[Mega](https://mega.nz/folder/eZkVQARa#YMElBWX7C3f_WYEKAKbBPQ)')
        embed1.add_field(name='LHPB',
                         value='[Mega](https://mega.nz/#!vFsmBapa!E99WYVHid24KtSPMWwYG3WYqOn1Xl1J3xO2-utJyvy0)')
        embed1.add_field(name='LICC', value='[Mega](https://mega.nz/#F!rFlACQAR!Es_L5lUy978lHkDjPOFJUg)')
        embed1.add_field(name='LIEE',
                         value='[Mega](https://mega.nz/#!TUkyEahZ!Z5hnAWwFtJPR_lKgm-PbtXpFHGl_UAID1DnglQFuQLo)')

        embed2 = discord.Embed(
            title='List of current available conversions',
            description='Please report broken/missing links, most of these are by Squawk7700 and require [SAM](https://forum.thresholdx.net/files/file/122-sam-scenery-animation-manager/)',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed2.set_footer(text='Page 2/3, use .c1 for page 1, .c3 for page 3')
        embed1.set_thumbnail(url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed2.add_field(name='LOWW', value='[Mega](https://mega.nz/#F!eccD3CyJ!2u4lNEYULLZOzPWZR-CB2Q)')
        embed2.add_field(name='MDPP', value='[Mega](https://mega.nz/#F!mN9EDYYR!RGvNGGqpkbxlUEyQcmXyfA)')
        embed2.add_field(name='MDSD',
                         value='[Mega](https://mega.nz/#!2Y8ywKTC!XejKD2ScqfgXK65jlxisqhzWfwKJab-vEWua2VcgY6w)')
        embed2.add_field(name='MDST',
                         value='[Mega](https://mega.nz/#!eAl0HQyQ!jmoab1OSThZ27rUpcYqlzMxCVwd9aOB2iVS0fSzttn4)')
        embed2.add_field(name='MTPP',
                         value='[Mega](https://mega.nz/#!OJtwAQYA!MhdCQIX3PqvGKKbY9VS4R5HUNSNh8v564L6UlTSMJhU)')
        embed2.add_field(name='OBBI',
                         value='[Mega](https://mega.nz/#!GAtkhKzK!FhRdS0VK-0NFpU_JUVM9qmQL3pxXa4xLiZ7JFO3rm9o)')
        embed2.add_field(name='OIIE',
                         value='[Mega](https://mega.nz/#!GypXHZqZ!PmpnSG8uUr59qRjMxXkSzGoXHn6cZ3Pn2RKHIPT0XRg)')
        embed2.add_field(name='OPLA',
                         value='[Mega](https://mega.nz/#!ndkmgKwZ!Yd5ZpfL9aV9rXAYN7r0HIcUkvlo2qiLs28dUTNN6C78)')
        embed2.add_field(name='PHOG',
                         value='[Mega](https://mega.nz/#!WBlS3Szb!CbbFRA02d-O4M6e71Zgp-qEal0Wsalh5DTJaKUrgnog)')
        embed2.add_field(name='RJAA', value='[Mega](https://mega.nz/#F!yQt0SQha!yZlmZ3MFEEQx8XRzPmPnBg)')

        embed3 = discord.Embed(
            title='List of current available conversions',
            description='Please report broken/missing links, most of these are by Squawk7700 and require [SAM](https://forum.thresholdx.net/files/file/122-sam-scenery-animation-manager/)',
            colour=discord.Colour.from_rgb(97, 0, 215)
        )

        embed3.set_footer(text='Page 3/3, use .c1 for page 1, .c2 for page 2')
        embed1.set_thumbnail(url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
        embed3.add_field(name='RJTT', value='[Mega](https://mega.nz/#F!jIsiSA4C!s5S4Ksx1rSXEpg5rl2kOKg)')
        embed3.add_field(name='SAEZ',
                         value='[Mega](https://mega.nz/#!ecsQwKgK!TRiUrD9eVQzJxTYihEKD372dMvGUgzs2Lc3_EzG1AU8)')
        embed3.add_field(name='SEQM',
                         value='[Mega](https://mega.nz/#!SU0iQCCT!n8vsPEipHm_FHn9eVO7f6ylSG9RfgJWOJgEd83GGVQE)')
        embed3.add_field(name='SEQU',
                         value='[Mega](https://mega.nz/#!2Nk00CqI!vKAyyIpyf8LH2Xsediv4WM__oLFelsEvfDzCRAlo9h0)')
        embed3.add_field(name='TFFR',
                         value='[Mega](https://mega.nz/#!HYkxTIIC!ADWUgLZJJpiwhbzDoRm_2JjcwciCmJMQMRMNqxSMH-A) || Requires [FlyBy Library](https://forums.x-plane.org/index.php?/files/file/28295-flyby-planes-library/)')
        embed3.add_field(name='TNCM',
                         value='[Mega](https://mega.nz/#!KI90RazD!0VEa7pBWuTPulbP-2Gnl3Yq-e820CtlunuBMNM2jHME)')
        embed3.add_field(name='VGHS',
                         value='[Mega](https://mega.nz/#!3I8XUQhK!DFJJZwxv1cBoXBHDYyv9_-4XQd3M5p0yWHHGckdnHC4)')
        embed3.add_field(name='VHHX',
                         value='[Mega](https://mega.nz/#!7V9kjIKQ!ViThWGnr_YSuVrcWAA7sKqjgssCUF0dYORn1xQ0dTxo)')
        embed3.add_field(name='VOBL', value='[Mega](https://mega.nz/folder/fdkRUaiB#a4Z3uBxBOT9vnWeqPhY31A)')

        await ctx.send(embed=embed1)

        @commands.command()
        async def c1():
            await ctx.channel.purge(limit=2)
            await ctx.send(embed=embed1)

        @commands.command()
        async def c2():
            await ctx.channel.purge(limit=2)
            await ctx.send(embed=embed2)

        @commands.command()
        async def c3():
            await ctx.channel.purge(limit=2)
            await ctx.send(embed=embed3)

    @commands.command()
    @check(guild_id)
    async def list(self, ctx):
        f = open('Private/Requests.txt', 'r')
        contents = f.read()
        await ctx.send(contents)
        f.close()

    @commands.command(aliases=['req'])
    @check(guild_id)
    async def request(self, ctx, *, request1):
        with open('Private/Requests.txt', 'a') as f:
            user = ctx.author
            req = str(request1)
            f.write(f'{user} = <{req}>\n')
            f.close()
        await ctx.send(f"Added '{request1}' to the request list, you can read the list with .list")

def setup(client):
    client.add_cog(Avia(client))
