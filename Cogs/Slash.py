import os
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, manage_commands
import requests
import json
from staticmap import StaticMap, CircleMarker, IconMarker

# from BravoOscarTango import get_prefix

avail_checklists = []

for checklists in os.listdir('./Utils/Checklists'):
    if checklists.endswith('.pdf'):
        avail_checklists.append(checklists[:-4])

with open('Private/WxAPI.txt', 'r') as x:
    xapi: str = x.read()
hdr = {"X-API-Key": xapi}

with open('Private/FPD.com API.txt', 'r') as q:
    fpd_api: str = q.read()

fltplan_id = 0

correct_sim_types = ['xplane11', 'xplane', 'fsx', 'fs9', 'pmdg', 'pdf']

guild_ids = []  # ids for slash commands


class Slash(commands.Cog):
    def __init__(self, client):
        self.bot = client

    # @cog_ext.cog_slash(name="test", guild_ids=guild_ids)
    # async def _test(self, ctx: SlashContext):
    #     embed = discord.Embed(title="embed test")
    #     await ctx.send(content="test", embeds=[embed])

    @cog_ext.cog_slash(name="charts",
                       description='Returns PDF chart for given airport ICAO',
                       options=[manage_commands.create_option(
                           name='icao',
                           description='Required airport ICAO code',
                           option_type=3,
                           required=True)], guild_ids=guild_ids)
    async def _charts(self, ctx: SlashContext, icao: str):

        # prfx = get_prefix(client=self, message=ctx.message)

        prfx = '/'

        print(f"Requested charts for {icao.upper()}")

        if len(icao) != 4:
            await ctx.send("ICAO code must be composed of 4 characters")
            return

        url = f"https://vau.aero/navdb/chart/{icao.upper()}.pdf"

        request = requests.get(url)

        if request.status_code != 200:
            await ctx.send(f"Error while retrieving charts for {icao.upper()}, try with another ICAO code")
        else:

            charts = discord.Embed(
                title=f"Requested charts for {icao.upper()}",
                description="[Link]({})".format(url)
            )
            charts.set_footer(
                text="You can also check the METAR for this airport with `{}metar {}`".format(prfx, icao.upper()))
            charts.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif")
            await ctx.send(embed=charts)

    @cog_ext.cog_slash(name='metar',
                       description='Fetches METAR for given airport ICAO',
                       options=[manage_commands.create_option(
                           name='icao',
                           description='Required airport ICAO code',
                           option_type=3,
                           required=True)],
                       guild_ids=guild_ids
                       )
    async def metar(self, ctx: SlashContext, icao: str):

        global gustbool
        if len(icao) != 4:
            await ctx.send("ICAO code must be composed of 4 characters")
            return

        req = requests.get('https://api.checkwx.com/metar/{}/decoded'.format(icao), headers=hdr)

        print(f"Requested METAR for {icao.upper()}")

        try:
            req.raise_for_status()
            resp = json.loads(req.text)

        except requests.exceptions.HTTPError as e:
            print(e)
            await ctx.send('Error occured:{}'.format(e))
            return

        if resp["results"] == 0:
            await ctx.send("No results, please check for typos or try a different ICAO")
            return

        # with open('./Utils/wx.json', 'w') as f:
        #     json.dump(resp, f, indent=4)

        layerint = len(resp["data"][0]["clouds"])  # integer for number of cloud layers

        wxint = len(resp["data"][0]["conditions"])  # presence of wx conditions

        visbool = "visibility" in resp["data"][0]  # presence of vis data

        if 'wind' in resp['data'][0]:
            gustbool = "gust_kts" in resp["data"][0]["wind"]  # presence of gusts
            wind_bool = True
        else:
            wind_bool = False

        name = resp["data"][0]["station"]["name"]
        if wind_bool:
            degrees = resp["data"][0]["wind"]["degrees"]
            speed = resp["data"][0]["wind"]["speed_kts"]
        temp = resp["data"][0]["temperature"]["celsius"]
        dew = resp["data"][0]["dewpoint"]["celsius"]
        humidity = resp["data"][0]["humidity"]["percent"]
        inhg = resp["data"][0]["barometer"]["hg"]
        hpa = resp["data"][0]["barometer"]["hpa"]
        obs = resp["data"][0]["observed"]
        cond = resp["data"][0]["flight_category"]
        raw = resp["data"][0]["raw_text"]

        points = []

        lat: float = resp["data"][0]["location"]["coordinates"][1]
        long: float = resp["data"][0]["location"]["coordinates"][0]

        points.append(tuple([lat, long]))

        marker_outline = CircleMarker((long, lat), 'white', 18)
        marker = CircleMarker((long, lat), '#0036FF', 12)
        icon_flag = IconMarker((long + 0.008, lat), './Utils/icon-flag.png', 12, 32)

        m = StaticMap(700, 300, 10, 10)
        m.add_marker(marker_outline)
        m.add_marker(marker)
        m.add_marker(icon_flag)

        image = m.render(zoom=8)
        image.save('Utils/metar.png')
        file = discord.File('Utils/metar.png')

        metar = discord.Embed(
            title="Requested METAR for {} - {}".format(icao.upper(), name),
            description="Raw: {}".format(raw),
            colour=discord.Colour.from_rgb(97, 0, 215)
        )
        if wind_bool:
            if not gustbool:
                metar.add_field(name="Wind:", value="{}° at {} kts".format(degrees, speed))
            else:
                gust = resp["data"][0]["wind"]["gust_kts"]
                metar.add_field(name="Wind:", value="{}° at {} kts, gusts {} kts".format(degrees, speed, gust))
        else:
            metar.add_field(name="Wind:", value="Calm")

        metar.add_field(name="Temp/Dewpoint:", value="{}°C/ {}°C".format(temp, dew))
        metar.add_field(name="Altimeter:", value="{} hPa/ {} inHg".format(hpa, inhg))
        if visbool:
            vismil = resp["data"][0]["visibility"]["miles"]
            vismet = resp["data"][0]["visibility"]["meters"]
            metar.add_field(name="Visibility:", value="{} meters/ {} miles".format(vismet, vismil))

        metar.add_field(name="Humidity:", value="{}%".format(humidity))
        metar.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif")
        metar.set_footer(text="Observed at {}. Flight category: {}".format(obs, cond))
        if wxint > 0:
            weather = resp["data"][0]["conditions"][0]["text"]
            metar.add_field(name="Weather condition:", value="{}".format(weather))

        if layerint == 1:
            clouds = resp["data"][0]["clouds"][0]["text"]
            if 'feet' in resp["data"][0]["clouds"][0]:
                clofeet = resp["data"][0]["clouds"][0]["feet"]
                metar.add_field(name="Cloud condition:", value="{}ft {}".format(clofeet, clouds))
            else:
                metar.add_field(name="Cloud condition:", value="{}".format(clouds))
        elif layerint == 2:
            clouds = resp["data"][0]["clouds"][0]["text"]
            clofeet = resp["data"][0]["clouds"][0]["feet"]
            clouds1 = resp["data"][0]["clouds"][1]["text"]
            clofeet1 = resp["data"][0]["clouds"][1]["feet"]
            metar.add_field(name="Cloud condition:",
                            value="{}ft {}/ {}ft {}".format(clofeet, clouds, clofeet1, clouds1))
        elif layerint == 3:
            clouds = resp["data"][0]["clouds"][0]["text"]
            clofeet = resp["data"][0]["clouds"][0]["feet"]
            clouds1 = resp["data"][0]["clouds"][1]["text"]
            clofeet1 = resp["data"][0]["clouds"][1]["feet"]
            clouds2 = resp["data"][0]["clouds"][2]["text"]
            clofeet2 = resp["data"][0]["clouds"][2]["feet"]
            metar.add_field(name="Cloud condition:",
                            value="{}ft {}/ {}ft {}/ {}ft {}".format(clofeet, clouds, clofeet1, clouds1, clofeet2,
                                                                     clouds2))
        else:
            metar.add_field(name="Cloud condition:", value="Not Specified / Cloud data error")

        metar.set_image(url='attachment://metar.png')

        await ctx.send(embed=metar, file=file)

    @cog_ext.cog_slash(name='flightplan',
                       description='Calculates a flight plan between two given airports',
                       options=[manage_commands.create_option(
                           name='dep',
                           description='Departure airport ICAO code',
                           option_type=3,
                           required=True),
                           manage_commands.create_option(
                               name='arr',
                               description='Arrival airport ICAO code',
                               option_type=3,
                               required=True)],
                       guild_ids=guild_ids
                       )
    async def flightplan(self, ctx: SlashContext, dep='lmfao', arr='lmfao'):

        # prfx = get_prefix(client=self, message=ctx.message)
        prfx = '/'

        if len(dep) != 4 or len(arr) != 4:
            await ctx.send('You need to specify two valid airport ICAO codes to create a flight plan')
            return

        loading = discord.Embed(
            title='Your flight plan is loading',
            description='Creating flight plan...'
        )
        loading.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif')
        loading.set_footer(text='Using data from the Flight Plan Database (https://flightplandatabase.com)')
        message = await ctx.send(embed=loading)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + fpd_api
        }
        data = '{"fromICAO":"immensecock","toICAO":"giganticpenis"}'
        data = data.replace("immensecock", dep)
        data = data.replace("giganticpenis", arr)
        print(f'Requested flight plan: {dep.upper()} to {arr.upper()}, generating...')

        response = requests.post('https://api.flightplandatabase.com/auto/generate', headers=headers, data=data)
        if response.status_code != 201:
            await message.delete()
            await ctx.send(
                f'There was an error while generating the flight plan: **{response.status_code}**, try with different ICAO codes')
            # self.flightplan.reset_cooldown(ctx)
            return

        plan = (str(response.json()))[7:14]
        print('Requesting...')

        loading1 = discord.Embed(
            title='Your flight plan is loading',
            description='Flight plan created successfully, uploading...'
        )
        loading1.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif')
        loading1.set_footer(text='Using data from the Flight Plan Database (https://flightplandatabase.com)')
        await message.delete()
        message1 = await ctx.send(embed=loading1)

        retrieve = requests.get(f'https://api.flightplandatabase.com/plan/{plan}')
        if retrieve.status_code != 200:
            await message1.delete()
            await ctx.send(
                f'There was an error while processing the flight plan: **{retrieve.status_code}**, try with different ICAO codes')
            # self.flightplan.reset_cooldown(ctx)
            return
        print('Received flight plan')

        flp = retrieve.json()
        flpid = flp['id']
        dep_icao = flp['fromICAO']
        arr_icao = flp['toICAO']
        dep_name = flp['fromName']
        arr_name = flp['toName']
        dist = int(flp['distance'])
        cr_alt = flp['maxAltitude']
        wpt_num = flp['waypoints']  # important
        link = f'https://flightplandatabase.com/plan/{flpid}'
        airac = flp['cycle']['ident']

        global fltplan_id

        fltplan_id = flpid

        i = 1
        route = f'***{dep_icao}***'
        route += ' ' + '[SID]'

        while i <= wpt_num:

            if flp['route']['nodes'][i]['ident'] != f'{arr_icao}':

                if flp['route']['nodes'][i]['ident'] == flp['route']['nodes'][i + 1]['ident']:
                    i += 1
                    continue
                elif flp['route']['nodes'][i]['via'] is None:
                    del flp['route']['nodes'][i]['via']
                    flp['route']['nodes'][i]['via'] = {}
                    flp['route']['nodes'][i]['via']['ident'] = 'None'
                    if i != 1:
                        if flp['route']['nodes'][i - 1]['via']['ident'] == 'None':
                            route += ' ' + '**DCT**' + ' ' + flp['route']['nodes'][i]['ident']
                        else:
                            route += ' ' + flp['route']['nodes'][i - 1]['ident'] + ' ' + '**DCT**' + ' ' + \
                                     flp['route']['nodes'][i]['ident']
                    else:
                        route += ' ' + flp['route']['nodes'][i]['ident']
                    i += 1
                    continue
                elif flp['route']['nodes'][i]['via']['ident'] != flp['route']['nodes'][i - 1]['via']['ident']:
                    if flp['route']['nodes'][i - 1]['via']['ident'] == 'None':
                        route += ' ' + '**DCT**' + ' ' + flp['route']['nodes'][i]['ident'] + ' ' + '**' + \
                                 flp['route']['nodes'][i]['via']['ident'] + '**'
                    else:
                        route += ' ' + flp['route']['nodes'][i]['ident'] + ' ' + '**' + flp['route']['nodes'][i]['via'][
                            'ident'] + '**'
                    i += 1
                    continue
                else:
                    i += 1
            else:
                route += ' ' + flp['route']['nodes'][i - 1]['ident'] + ' ' + '[STAR]' + ' '
                route += f'***{arr_icao}***'
                break

        flp_embed = discord.Embed(
            title=f"Here's your flight plan: **{dep_icao} → {arr_icao}**",
            description=f"Flight plan: {route}"
        )
        flp_embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif')
        flp_embed.add_field(name='Departure Airport:', value=dep_name)
        flp_embed.add_field(name='Arrival Airport:', value=arr_name)
        flp_embed.add_field(name='Distance / Cruise Altitude:', value=f'{dist}nm/{cr_alt}ft')
        flp_embed.add_field(name='Link to full flight plan:', value=link)
        flp_embed.set_footer(
            text=f'Using data from the Flight Plan Database (https://flightplandatabase.com), AIRAC Cycle: {airac[3:]}, download the flight plan with {prfx}download')

        print('Success!')
        await message1.delete()
        await ctx.send(embed=flp_embed)

    @cog_ext.cog_slash(name='checklist',
                       description='Returns checklist for supported a aircraft',
                       options=[manage_commands.create_option(
                           name='plane',
                           description='Required aircraft ICAO code',
                           option_type=3,
                           required=False)],
                       guild_ids=guild_ids
                       )
    async def checklist(self, ctx: SlashContext, plane='avail'):

        # prfx = get_prefix(client=self, message=ctx.message)
        prfx = '/'

        if plane == 'avail':
            avplanes = ', '.join(avail_checklists)
            await ctx.send(f'Checklists are currenly available for these planes: **{avplanes}**')

        elif len(plane) != 4:
            await ctx.send(
                f"You must input a correct 4 character ICAO code for your plane, check available checklists with {prfx}checklist (empty argument)")
        elif plane.upper() in avail_checklists:
            clfile = discord.File(f'./Utils/Checklists/{plane.upper()}.pdf')
            await ctx.send(f"Here's your requested checklist for the {plane.upper()}:", file=clfile)
        else:
            await ctx.send(
                f"Unfortunately the checklist you requested is not available, check a list of available checklists with {prfx}checklist (empty argument)")

    @cog_ext.cog_slash(name='download',
                       description='Downloads a generated FMS plan in a given format, requires a flight plan to be created (/flightplan)',
                       options=[manage_commands.create_option(
                           name='sim_type',
                           description='Required file format for the flight plan, leave blank for a list of options',
                           option_type=3,
                           required=False)],
                       guild_ids=guild_ids)
    async def download(self, ctx: SlashContext, sim_type='None'):

        # prfx = get_prefix(client=self, message=ctx.message)
        prfx = '/'

        if fltplan_id == 0:
            await ctx.send(f'You need to first create a flight plan with {prfx}flightplan')
            return
        elif sim_type.lower() not in correct_sim_types:
            await ctx.send('You need to specify a correct file format, supported formats are: xplane11 [X-Plane 11], xplane [X-Plane 10], fsx [FSX], fs9 [FS2004], pmdg [PMDG], pdf [PDF]')
            return
        else:
            download_embed = discord.Embed(
                title=f'Requested flight plan for {sim_type.upper()}',
                description=f'To download the file click [here](https://www.flightplandatabase.com/plan/{fltplan_id}/download/{sim_type.lower()})'
            )
            download_embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif')
            download_embed.set_footer(text=f'Using data from the Flight Plan Database (https://flightplandatabase.com)')
            await ctx.send(embed=download_embed)


def setup(client):
    client.add_cog(Slash(client))
