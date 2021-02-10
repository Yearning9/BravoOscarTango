import random
import requests
import json
import discord
import os
from zalgo_text import zalgo
from markovbot import MarkovBot
from pathlib import Path
from discord.ext import commands
import google_images_search
from discord.ext.commands import MissingRequiredArgument, CommandOnCooldown
from PIL import Image, ImageDraw, ImageFont

funbot = MarkovBot()

dirname = os.path.dirname(os.path.abspath(__file__))



book = os.path.join(dirname, u'../Utils/manifesto.txt')


with open('Private/Gis1.txt', 'r') as q:
    gis1: str = q.read()

with open('Private/Gis2.txt', 'r') as w:
    gis2: str = w.read()

with open('Private/APIkey.txt', 'r') as e:
    apikey: str = e.read()

gis = google_images_search.GoogleImagesSearch(gis1, gis2)

lmt = 1


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['mk'])
    async def markov(self, ctx):
        funbot.read(book)
        n = random.randint(2, 40)
        text = funbot.generate_text(n)
        await ctx.send(text)

    @commands.command(aliases=['z'])
    async def zalgo(self, ctx, *, text: str):
        await ctx.send(zalgo.zalgo().zalgofy(text))

    # @commands.command()
    # async def pray(self, ctx, *, text: str = 'None'):
    #
    #     if text != 'None':
    #         if text.lower() == 'colonialism':
    #             return await ctx.send(':(')
    #         if len(text) <= 11:
    #             img = Image.open('Utils/vuling.jpg')
    #             draw = ImageDraw.Draw(img)
    #             font = ImageFont.truetype('./Utils/font.ttf', 50)
    #             draw.text((175, 0), 'Vuling loves ' + text, (116, 116, 116), font=font)
    #             draw.text((15, 450), 'Because Vuling loves everybody ♥', (116, 116, 116), font=font)
    #             img.save('Utils/vuling_out.jpg')
    #             vuling_pic = discord.File('./Utils/vuling_out.jpg')
    #             await ctx.send(file=vuling_pic)
    #         elif 11 < len(text) <= 20:
    #             img = Image.open('Utils/vuling.jpg')
    #             draw = ImageDraw.Draw(img)
    #             font = ImageFont.truetype('./Utils/font.ttf', 50)
    #             draw.text((175, 0), 'Vuling loves\n' + text, (116, 116, 116), font=font)
    #             draw.text((15, 450), 'Because Vuling loves everybody ♥', (116, 116, 116), font=font)
    #             img.save('Utils/vuling_out.jpg')
    #             vuling_pic = discord.File('./Utils/vuling_out.jpg')
    #             await ctx.send(file=vuling_pic)
    #         else:
    #             await ctx.reply('Text is too long, max 20 characters', mention_author=False)
    #     else:
    #         await ctx.reply('You need to specify some text!', mention_author=False)


    @commands.command()
    @commands.cooldown(1, 5)
    async def pic(self, ctx, *, image_query):
        async with ctx.typing():
            if os.path.exists('./Utils/image.jpg'):
                os.remove('./Utils/image.jpg')
            _search_params = {'q': image_query, 'num': 1, 'safe': 'medium', 'fileType': 'jpg'}
            gis.search(search_params=_search_params, path_to_dir='./Utils/', custom_image_name='image')
            image = discord.File('Utils/image.jpg')
            size = Path('Utils/image.jpg').stat().st_size
            if size > 8388119:
                return await ctx.reply('Image is too big for Discord! Try a different search', mention_author=False)

            await ctx.reply(file=image, mention_author=False)

    # @commands.command()
    # async def vuling(self, ctx):
    #     await ctx.reply('***ALL PRAISE OUR LORD AND SAVIOR VULING***  https://cdn.discordapp.com/attachments/680058574990475444/705384663903895564/EC-MBT_A320_Vueling_BCN.png', mention_author=False)
    #
    # @commands.command()
    # async def md11(self, ctx):
    #     await ctx.reply('https://cdn.discordapp.com/attachments/689441452920537120/738870438406389840/Look_at_the_MD-11.mp4', mention_author=False)

    @commands.command()
    async def garloc(self, ctx):
        with open('Utils/messages.txt', 'r') as f:
            messages = [line.rstrip() for line in f]
        await ctx.channel.send(f'{random.choice(messages)}')

    # @commands.command()
    # async def colonialism(self, ctx):
    #     await ctx.reply('https://media.discordapp.net/attachments/696375145127739442/737247675912552458/KAPPA3041327.jpg', mention_author=False)

    @commands.command(aliases=['g'])
    async def gif(self, ctx, *, search_term):

        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
        if r.status_code == 200:
            gifs = json.loads(r.content)
            url = gifs["results"][0]["url"]
            await ctx.reply(url, mention_author=False)
        else:
            await ctx.reply("Couldn't find a GIF", mention_author=False)

    @gif.error
    async def gif_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.reply('https://cdn.discordapp.com/attachments/356779184393158657/737319352654757888/ezgif.com-optimize.gif', mention_author=False)

    @pic.error
    async def pic_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.reply('You need to specify an image to search', mention_author=False)
        if isinstance(error, CommandOnCooldown):
            await ctx.reply('Command on cooldown, please wait a few seconds', mention_author=False)

def setup(client):
    client.add_cog(Fun(client))
