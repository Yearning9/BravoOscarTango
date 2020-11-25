from discord.ext import commands
import requests
# from opensky_api import OpenSkyApi
import discord
# import flightradar24
import json

# from datetime import datetime
from staticmap import StaticMap, CircleMarker, IconMarker

# osapi = OpenSkyApi()
# fr = flightradar24.Api()

with open('Private/WxAPI.txt', 'r') as x:
    xapi: str = x.read()
hdr = {"X-API-Key": xapi}


class Flights(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["wx"])
    async def metar(self, ctx, icao: str):
        req = requests.get('https://api.checkwx.com/metar/{}/decoded'.format(icao), headers=hdr)

        icao = icao.upper()
        print("Requested METAR for {}".format(icao))

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

        layerint = len(resp["data"][0]["clouds"])       # integer for number of cloud layers
        wxint = len(resp["data"][0]["conditions"])      # presence of wx conditions
        visbool = "visibility" in resp["data"][0]       # presence of vis data
        gustbool = "gust_kts" in resp["data"][0]["wind"]  # presence of gusts

        name = resp["data"][0]["station"]["name"]
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

        print(lat, long)

        points.append(tuple([lat, long]))

        marker_outline = CircleMarker((long, lat), 'white', 18)
        marker = CircleMarker((long, lat), '#0036FF', 12)
        icon_flag = IconMarker((long, lat), './Utils/icon-flag.png', 12, 32)

        m = StaticMap(700, 300, 10, 10)
        m.add_marker(marker_outline)
        m.add_marker(marker)
        m.add_marker(icon_flag)

        image = m.render(zoom=8)
        image.save('Utils/metar.png')
        file = discord.File('Utils/metar.png')


        metar = discord.Embed(
            title="Requested METAR for {} - {}".format(icao, name),
            description="Raw: {}".format(raw),
            colour=discord.Colour.from_rgb(97, 0, 215)
        )
        if not gustbool:
            metar.add_field(name="Wind:", value="{}° at {} kts".format(degrees, speed))
        else:
            gust = resp["data"][0]["wind"]["gust_kts"]
            metar.add_field(name="Wind:", value="{}° at {} kts, gusts {} kts".format(degrees, speed, gust))
        metar.add_field(name="Temp/Dewpoint:", value="{}°C/ {}°C".format(temp, dew))
        metar.add_field(name="Altimeter:", value="{} hPa/ {} inHg".format(hpa, inhg))
        if visbool:
            vismil = resp["data"][0]["visibility"]["miles"]
            vismet = resp["data"][0]["visibility"]["meters"]
            metar.add_field(name="Visibility:", value="{} meters/ {} miles".format(vismet, vismil))
        metar.add_field(name="Humidity:", value="{}%".format(humidity))
        metar.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/356779184393158657/729351510974267513/plane-travel-icon-rebound2.gif")
        metar.set_footer(text="Observed at {}. Flight category: {}".format(obs, cond))
        if wxint > 0:
            weather = resp["data"][0]["conditions"][0]["text"]
            metar.add_field(name="Weather condition:", value="{}".format(weather))

        if layerint == 1:
            clouds = resp["data"][0]["clouds"][0]["text"]
            clofeet = resp["data"][0]["clouds"][0]["feet"]
            metar.add_field(name="Cloud condition:", value="{}ft {}".format(clofeet, clouds))
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
                            value="{}ft {}/ {}ft {}/ {}ft {}".format(clofeet, clouds, clofeet1, clouds1, clofeet2, clouds2))
        elif layerint == 0:
            metar.add_field(name="Cloud condition:", value="None/ Not Specified")

        metar.set_image(url='attachment://metar.png')

        await ctx.send(embed=metar, file=file)

    # @commands.command()
    # async def flight(self, ctx):
    #     states = osapi.get_states()
    #     print(states)
    #     flight_data = json.loads(states)
    #     print(flight_data)
    #     await ctx.send('Saved flights as json')

    @commands.command(aliases=['ff'])
    async def fr24(self, ctx):  # add flight_id after ctx

        await ctx.send("Unfortunately FlightRadar24 integration is not available anymore")

        # flight = fr.get_flight(flight_id)
        #
        # json_str = json.dumps(flight)
        # flight_data = json.loads(json_str)
        # data = flight_data["result"]["response"]["data"]
        # airline = data[0]["airline"]["name"]
        # numbers = flight_data["result"]["response"]["item"]["current"]
        # query = flight_data["result"]["request"]["query"]
        # timestamp = flight_data["result"]["response"]["timestamp"]
        #
        # ts = datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        #
        # live_list = ''
        # for i in data:
        #     live_list += '{}\n'.format(i["status"]["live"])
        # with open('Utils/live.txt', 'w') as f:
        #     f.write(live_list)
        #
        # word = 'True'
        # lime: int = 0
        # with open('Utils/live.txt', 'r') as f:
        #     for i, line in enumerate(f):
        #         if word in line:
        #             lime = i
        #
        # j: int = lime + 1
        # plane = data[j]["aircraft"]["model"]["text"]
        #
        # if live_list.find('True') != -1:                                                                      # wow this is a long if statement
        #     origin = data[j]["airport"]["origin"]["code"]["icao"]
        #     destination = data[j]["airport"]["destination"]["code"]["icao"]
        #     plane_pic = flight_data["result"]["response"]["aircraftImages"][0]["images"]["large"][0]["src"]
        #     registration = data[j]["aircraft"]["registration"]
        #     time = data[j]["time"]
        #     origin_country = data[j]["aircraft"]["country"]["alpha2"]
        #     flag = origin_country.lower()
        #     callsign = data[j]["identification"]["callsign"]
        #
        #
        #     schedu1 = time["scheduled"]["departure"]  # scheduled dep in unix
        #     schedu2 = time["scheduled"]["arrival"]  # scheduled arr in unix
        #     actu = time["real"]["departure"]  # real dep in unix
        #     etau = time["other"]["eta"]  # estimated arr in unix
        #     sched1 = datetime.utcfromtimestamp(schedu1).strftime('%d-%m %H:%M')
        #     sched2 = datetime.utcfromtimestamp(schedu2).strftime('%d-%m %H:%M')
        #     act = datetime.utcfromtimestamp(actu).strftime('%d-%m %H:%M')
        #     eta = datetime.utcfromtimestamp(etau).strftime('%d-%m %H:%M')
        #
        #     points = []
        #
        #     lat1 = data[j]["airport"]["origin"]["position"]["latitude"]
        #     long1 = data[j]["airport"]["origin"]["position"]["longitude"]
        #     lat2 = data[j]["airport"]["destination"]["position"]["latitude"]
        #     long2 = data[j]["airport"]["destination"]["position"]["longitude"]
        #
        #     points.append(tuple([long1, lat1]))
        #     points.append(tuple([long2, lat2]))
        #
        #     m = StaticMap(400, 400, 20, 20)
        #     m.add_line(Line(points, 'blue', 3))
        #     icon_flag = IconMarker((long2, lat2), './Utils/icon-flag.png', 12, 32)
        #     marker_outline = CircleMarker((long1, lat1), 'white', 18)
        #     marker = CircleMarker((long1, lat1), 'black', 12)
        #     m.add_marker(icon_flag)
        #     m.add_marker(marker_outline)
        #     m.add_marker(marker)
        #
        #     image = m.render()
        #     image.save('Utils/map.png')
        #
        #
        #     file = discord.File('Utils/map.png')
        #
        #     if airline == 'Vueling':
        #         airline = 'Vuling'
        #
        #
        #     live_flight = discord.Embed(
        #         title='{} [{} | {}]'.format(airline, query, callsign),
        #         description='**{} → {}**'.format(origin, destination),
        #         colour=discord.Colour.from_rgb(97, 0, 215)
        #     )
        #     live_flight.set_thumbnail(url='{}'.format(plane_pic))
        #     live_flight.set_footer(text='Copyright © 2014-2020 Flightradar24 AB.')
        #     live_flight.add_field(name='Aircraft type:', value='{}'.format(plane))
        #     live_flight.add_field(name='Registration:', value=':flag_{}: - {}'.format(flag, registration))
        #     live_flight.add_field(name='Scheduled/Actual Departure:', value='{} / {}'.format(sched1, act), inline=False)
        #     live_flight.add_field(name='Scheduled/Estimated Arrival:', value='{} / {}'.format(sched2, eta), inline=True)
        #     live_flight.set_image(url='attachment://map.png')
        #     await ctx.send(embed=live_flight, file=file)
        #     if airline == 'Vuling':
        #         await ctx.send('*:pray: Pray for our lord Vuling :pray:*')
        #     return
        #
        #
        # else:
        #     await ctx.send('The flight you requested is not currently live, I have found {} scheduled/past flights'.format(numbers))
        #
        #     lista = ''
        #
        #     for i in data:
        #         print(i["aircraft"]["model"]["code"], i["aircraft"]["model"]["text"], i["status"]["text"])
        #         status = i["status"]["text"]
        #         stdu = i["time"]["scheduled"]["departure"]
        #         std = datetime.utcfromtimestamp(stdu).strftime('%d-%m %H:%M')
        #         lista += '{}, Scheduled: {} - Status: {}\n'.format(i["aircraft"]["model"]["code"], std, status)
        #
        #     embed = discord.Embed(
        #         title='{} flight {}'.format(airline, query),
        #         description='\n{}'.format(lista)
        #     )
        #     embed.set_footer(text='Updated at {} UTC'.format(ts))
        #
        #     await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Flights(client))
