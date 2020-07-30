import discord
from covid import Covid
from discord.ext import commands

covid = Covid()



class Virus(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def covid(self, ctx, *, country: str = 'None'):

        if country == 'None':
            virus = covid.get_data()
            country_high = virus[0]["country"]
            country_high_act = virus[0]["active"]
            country_high_cases = virus[0]["confirmed"]
            country_high_recovered = virus[0]["recovered"]
            country_high_deaths = virus[0]["deaths"]



            vembed = discord.Embed(
                title='Country with most cases is {}'.format(country_high),
                colour=discord.Colour.from_rgb(97, 0, 215)
                )

            vembed.set_thumbnail(url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
            vembed.add_field(name='Confirmed cases:', value=country_high_cases)
            vembed.add_field(name='Active cases:', value=country_high_act)
            vembed.add_field(name='Recovered cases:', value=country_high_recovered)
            vembed.add_field(name='Total deaths', value=country_high_deaths)
            vembed.set_footer(text='Data from John Hopkins University')

            await ctx.send(embed=vembed)

        else:
            virus_country = covid.get_status_by_country_name(country)
            country_name = virus_country['country']
            country_act = virus_country['active']
            country_cases = virus_country['confirmed']
            country_recovered = virus_country['recovered']
            country_deaths = virus_country['deaths']


            vembed1 = discord.Embed(
                title='Covid19 data for {}'.format(country_name),
                colour=discord.Colour.from_rgb(97, 0, 215)
            )

            vembed1.set_thumbnail(url='https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif')
            vembed1.add_field(name='Confirmed cases:', value=country_cases)
            vembed1.add_field(name='Active cases:', value=country_act)
            vembed1.add_field(name='Recovered cases:', value=country_recovered)
            vembed1.add_field(name='Total deaths', value=country_deaths)
            vembed1.set_footer(text='Data from John Hopkins University')

            await ctx.send(embed=vembed1)


def setup(client):
    client.add_cog(Virus(client))
