from discord.ext import commands
import discord
import flightradar24
import json
from datetime import datetime
from staticmap import StaticMap, Line, IconMarker, CircleMarker

fr = flightradar24.Api()


class Flights(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ff'])
    async def flight(self, ctx, flight_id):

        flight = fr.get_flight(flight_id)

        json_str = json.dumps(flight)
        flight_data = json.loads(json_str)
        data = flight_data["result"]["response"]["data"]
        airline = data[0]["airline"]["name"]
        numbers = flight_data["result"]["response"]["item"]["current"]
        query = flight_data["result"]["request"]["query"]
        timestamp = flight_data["result"]["response"]["timestamp"]

        ts = datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')

        live_list = ''
        for i in data:
            live_list += '{}\n'.format(i["status"]["live"])
        with open('Utils/live.txt', 'w') as f:
            f.write(live_list)

        word = 'True'
        lime: int = 0
        with open('Utils/live.txt', 'r') as f:
            for i, line in enumerate(f):
                if word in line:
                    lime = i

        j: int = lime + 1
        plane = data[j]["aircraft"]["model"]["text"]

        if live_list.find('True') != -1:                                                                      # wow this is a long if statement
            origin = data[j]["airport"]["origin"]["code"]["icao"]
            destination = data[j]["airport"]["destination"]["code"]["icao"]
            plane_pic = flight_data["result"]["response"]["aircraftImages"][0]["images"]["large"][0]["src"]
            registration = data[j]["aircraft"]["registration"]
            time = data[j]["time"]
            origin_country = data[j]["aircraft"]["country"]["alpha2"]
            flag = origin_country.lower()
            callsign = data[j]["identification"]["callsign"]


            schedu1 = time["scheduled"]["departure"]  # scheduled dep in unix
            schedu2 = time["scheduled"]["arrival"]  # scheduled arr in unix
            actu = time["real"]["departure"]  # real dep in unix
            etau = time["other"]["eta"]  # estimated arr in unix
            sched1 = datetime.utcfromtimestamp(schedu1).strftime('%d-%m %H:%M')
            sched2 = datetime.utcfromtimestamp(schedu2).strftime('%d-%m %H:%M')
            act = datetime.utcfromtimestamp(actu).strftime('%d-%m %H:%M')
            eta = datetime.utcfromtimestamp(etau).strftime('%d-%m %H:%M')

            points = []

            lat1 = data[j]["airport"]["origin"]["position"]["latitude"]
            long1 = data[j]["airport"]["origin"]["position"]["longitude"]
            lat2 = data[j]["airport"]["destination"]["position"]["latitude"]
            long2 = data[j]["airport"]["destination"]["position"]["longitude"]

            points.append(tuple([long1, lat1]))
            points.append(tuple([long2, lat2]))

            m = StaticMap(400, 400, 20, 20)
            m.add_line(Line(points, 'blue', 3))
            icon_flag = IconMarker((long2, lat2), './Utils/icon-flag.png', 12, 32)
            marker_outline = CircleMarker((long1, lat1), 'white', 18)
            marker = CircleMarker((long1, lat1), 'black', 12)
            m.add_marker(icon_flag)
            m.add_marker(marker_outline)
            m.add_marker(marker)

            image = m.render()
            image.save('Utils/map.png')


            file = discord.File('Utils/map.png')

            if airline == 'Vueling':
                airline = 'Vuling'


            live_flight = discord.Embed(
                title='{} [{} | {}]'.format(airline, query, callsign),
                description='**{} → {}**'.format(origin, destination),
                colour=discord.Colour.from_rgb(97, 0, 215)
            )
            live_flight.set_thumbnail(url='{}'.format(plane_pic))
            live_flight.set_footer(text='Copyright © 2014-2020 Flightradar24 AB.')
            live_flight.add_field(name='Aircraft type:', value='{}'.format(plane))
            live_flight.add_field(name='Registration:', value=':flag_{}: - {}'.format(flag, registration))
            live_flight.add_field(name='Scheduled/Actual Departure:', value='{} / {}'.format(sched1, act), inline=False)
            live_flight.add_field(name='Scheduled/Estimated Arrival:', value='{} / {}'.format(sched2, eta), inline=True)
            live_flight.set_image(url='attachment://map.png')
            await ctx.send(embed=live_flight, file=file)
            if airline == 'Vuling':
                await ctx.send('*:pray: Pray for our lord Vuling :pray:*')
            return


        else:
            await ctx.send('The flight you requested is not currently live, I have found {} scheduled/past flights'.format(numbers))

            lista = ''

            for i in data:
                print(i["aircraft"]["model"]["code"], i["aircraft"]["model"]["text"], i["status"]["text"])
                status = i["status"]["text"]
                stdu = i["time"]["scheduled"]["departure"]
                std = datetime.utcfromtimestamp(stdu).strftime('%d-%m %H:%M')
                lista += '{}, Scheduled: {} - Status: {}\n'.format(i["aircraft"]["model"]["code"], std, status)

            embed = discord.Embed(
                title='{} flight {}'.format(airline, query),
                description='\n{}'.format(lista)
            )
            embed.set_footer(text='Updated at {} UTC'.format(ts))

            await ctx.send(embed=embed)
            return


def setup(client):
    client.add_cog(Flights(client))
