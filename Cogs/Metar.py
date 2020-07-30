
##import
from typing import Any, Union, List
from discord.ext import commands
import csv
import urllib3
import io
##setup
http = urllib3.PoolManager()
urllib3.disable_warnings()
###r = http.request('GET', 'https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=csv&stationString=KDEN&hoursBeforeNow=2', preload_content=False)
###r.auto_close = False
##first command##
class Metar(commands.Cog):
        def __init__(self, client):
                self.client = client
        @commands.command(aliases=['metar'])
        async def metars(self, ctx, airportul, time='1', page: int = 1):
                airport = str.lower(airportul)
                response = http.request('GET', 'https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=csv&stationString=' + airport + '&hoursBeforeNow=' + time)
                print(response.data)
                #with open(response.data, newline='\n\r') as csvfile:
                        #reader = csv.reader(csvfile, delimiter=',')
                        #for row in reader:
                            #print(row)
                print(response.data)  # Raw data.

def setup(client):
    client.add_cog(Metar(client))