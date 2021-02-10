from discord.ext import commands
import requests
import discord
import json
import os
from staticmap import StaticMap, CircleMarker, IconMarker
# from WonderfulBot import guild_prefix


prfx = '.'

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

class FlightSim(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["wx"])
    @commands.cooldown(1, 3)
    async def metar(self, ctx, icao: str):

        global gustbool
        if len(icao) != 4:
            await ctx.reply("ICAO code must be composed of 4 characters", mention_author=False)
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

    @commands.command(aliases=["chart", "ch"])
    async def charts(self, ctx, icao1: str):

        with ctx.typing():
            print(f"Requested charts for {icao1.upper()}")

            if len(icao1) != 4:
                await ctx.reply("ICAO code must be composed of 4 characters", mention_author=False)
                return

            url = f"https://vau.aero/navdb/chart/{icao1.upper()}.pdf"

            request = requests.get(url)

            if request.status_code != 200:
                await ctx.reply(f"Error while retrieving charts for {icao1.upper()}, try with another ICAO code",
                                mention_author=False)
            else:

                charts = discord.Embed(
                    title=f"Requested charts for {icao1.upper()}",
                    description="[Link]({})".format(url)
                )
                charts.set_footer(
                    text="You can also check the METAR for this airport with `{}metar {}`".format(prfx, icao1.upper()))
                charts.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif")
                await ctx.reply(embed=charts, mention_author=False)
                return

    @commands.command(aliases=["cl"])
    async def checklist(self, ctx, plane='avail'):

        if plane == 'avail':
            avplanes = ', '.join(avail_checklists)
            await ctx.reply(f'Checklists are currenly available for these planes: **{avplanes}**', mention_author=False)

        elif len(plane) != 4:
            await ctx.reply(
                f"You must input a correct 4 character ICAO code for your plane, check available checklists with {prfx}cl",
                mention_author=False)
        elif plane.upper() in avail_checklists:
            clfile = discord.File(f'./Utils/Checklists/{plane.upper()}.pdf')
            await ctx.reply(f"Here's your requested checklist for the {plane.upper()}:", file=clfile,
                            mention_author=False)
        else:
            await ctx.reply(
                "Unfortunately the checklist you requested is not available, check a list of available checklists with .cl",
                mention_author=False)

    @commands.command(aliases=['fl', 'flp', 'fltplan'])
    @commands.cooldown(1, 10)
    async def flightplan(self, ctx, dep='lmfao', arr='lmfao'):

        if dep == 'lmfao' or arr == 'lmfao':
            await ctx.send('You need to specify two valid airport ICAO codes to create a flight plan')
            self.flightplan.reset_cooldown(ctx)
            return
        elif len(dep) != 4 or len(arr) != 4:
            await ctx.send('You need to specify two valid airport ICAO codes to create a flight plan')
            self.flightplan.reset_cooldown(ctx)
            return

        loading = discord.Embed(
            title='Your flight plan is loading',
            description='Creating flight plan...'
        )
        loading.set_thumbnail(url='https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif')
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
            await ctx.send(f'There was an error while generating the flight plan: **{response.status_code}**, try with different ICAO codes')
            self.flightplan.reset_cooldown(ctx)
            return

        plan = (str(response.json()))[7:14]
        print('Requesting...')

        loading1 = discord.Embed(
            title='Your flight plan is loading',
            description='Flight plan created successfully, uploading...'
        )
        loading1.set_thumbnail(url='https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif')
        loading1.set_footer(text='Using data from the Flight Plan Database (https://flightplandatabase.com)')
        await message.delete()
        message1 = await ctx.send(embed=loading1)

        retrieve = requests.get(f'https://api.flightplandatabase.com/plan/{plan}')
        if retrieve.status_code != 200:
            await message1.delete()
            await ctx.send(f'There was an error while processing the flight plan: **{retrieve.status_code}**, try with different ICAO codes')
            self.flightplan.reset_cooldown(ctx)
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
        wpt_num = flp['waypoints']    # important
        link = f'https://flightplandatabase.com/plan/{flpid}'
        airac = flp['cycle']['ident']

        global fltplan_id

        fltplan_id = flpid


        i = 1
        route = f'***{dep_icao}***'
        route += ' ' + '[SID]'

        while i <= wpt_num:

            if flp['route']['nodes'][i]['ident'] != f'{arr_icao}':

                if flp['route']['nodes'][i]['ident'] == flp['route']['nodes'][i+1]['ident']:
                    i += 1
                    continue
                elif flp['route']['nodes'][i]['via'] is None:
                    print(flp['route']['nodes'][i]['ident'])
                    del flp['route']['nodes'][i]['via']
                    flp['route']['nodes'][i]['via'] = {}
                    flp['route']['nodes'][i]['via']['ident'] = 'None'
                    print(flp['route']['nodes'][i]['via']['ident'])
                    if i != 1:
                        if flp['route']['nodes'][i-1]['via']['ident'] == 'None':
                            route += ' ' + '**DCT**' + ' ' + flp['route']['nodes'][i]['ident']
                        else:
                            route += ' ' + flp['route']['nodes'][i-1]['ident'] + ' ' + '**DCT**' + ' ' + flp['route']['nodes'][i]['ident']
                    else:
                        route += ' ' + flp['route']['nodes'][i]['ident']
                    i += 1
                    continue
                elif flp['route']['nodes'][i]['via']['ident'] != flp['route']['nodes'][i-1]['via']['ident']:
                    print(flp['route']['nodes'][i]['via']['ident'])
                    if flp['route']['nodes'][i-1]['via']['ident'] == 'None':
                        route += ' ' + '**DCT**' + ' ' + flp['route']['nodes'][i]['ident'] + ' ' + '**' + flp['route']['nodes'][i]['via']['ident'] + '**'
                    else:
                        route += ' ' + flp['route']['nodes'][i]['ident'] + ' ' + '**' + flp['route']['nodes'][i]['via']['ident'] + '**'
                    i += 1
                    continue
                else:
                    i += 1
            else:
                route += ' ' + flp['route']['nodes'][i-1]['ident'] + ' ' + '[STAR]' + ' '
                route += f'***{arr_icao}***'
                break

        print(route)

        flp_embed = discord.Embed(
            title=f"Here's your flight plan: **{dep_icao} → {arr_icao}**",
            description=f"Flight plan: {route}"
        )
        flp_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif')
        flp_embed.add_field(name='Departure Airport:', value=dep_name)
        flp_embed.add_field(name='Arrival Airport:', value=arr_name)
        flp_embed.add_field(name='Distance / Cruise Altitude:', value=f'{dist}nm/{cr_alt}ft')
        flp_embed.add_field(name='Link to full flight plan:', value=link)
        flp_embed.set_footer(text=f'Using data from the Flight Plan Database (https://flightplandatabase.com), AIRAC Cycle: {airac[3:]}, download the flight plan with {prfx}download')

        await message1.delete()
        await ctx.send(embed=flp_embed)

    @commands.command()
    async def download(self, ctx, sim_type='None'):
        if fltplan_id == 0:
            await ctx.reply(f'You need to first create a flight plan with {prfx}flightplan', mention_author=False)
            return
        elif sim_type not in correct_sim_types:
            await ctx.reply('You need to specify a correct file format, supported formats are: xplane11 [X-Plane 11], xplane [X-Plane 10], fsx [FSX], fs9 [FS2004], pmdg [PMDG], pdf [PDF]', mention_author=False)
            return
        else:
            download_embed = discord.Embed(
                title=f'Requested flight plan for {sim_type.upper()}',
                description=f'To download the file click [here](https://www.flightplandatabase.com/plan/{fltplan_id}/download/{sim_type.lower()})'
            )
            download_embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/651086904925749252/802617703809548298/ezgif.com-gif-maker_3.gif')
            download_embed.set_footer(text=f'Using data from the Flight Plan Database (https://flightplandatabase.com)')
            await ctx.reply(embed=download_embed, mention_author=False)

    @flightplan.error
    async def flp_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.reply('Command on cooldown, please wait a few seconds or wait for the current request to be processed', mention_author=False, delete_after=10)

    @metar.error
    async def metar_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.reply('Command on cooldown, please wait a few seconds or wait for the current request to be processed', mention_author=False, delete_after=5)

def setup(client):
    client.add_cog(FlightSim(client))
