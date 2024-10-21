import discord
from discord import Embed
from discord.ext import commands

import aiohttp
import urllib
import requests
from bs4 import *
import json
import random
from datetime import *

async def setup(bot) -> None:
    await bot.add_cog(api(bot))

class api(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ditmenavi_load()

    #ham api dep trai
    @staticmethod
    async def _request(url : str, **kwrags):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, **kwrags) as response:
                return await response.json()

    @commands.is_nsfw()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = 'randomorz')
    async def randomorz(self, ctx:commands.Context):
        """forbidden command 🥵⚠️"""

        COUNDNT_FOUND_RESULT = 'https://images-ext-1.discordapp.net/external/AUKM52nm37_7bqv0souTdSHEkCaDHeVft8bAITfLFpE/https/cdn.discordapp.com/emojis/941346145022672946.png'

        params = {
            'api_key': 'rfk9wx4ZQkcmPnU1fhZru11h',
            'login': 'iuuahct'
        }
        resp = await self._request('https://danbooru.donmai.us/posts/random.json',params=params)
        

        await ctx.reply(
            embed=Embed().set_image(
                url=resp.get('large_file_url', COUNDNT_FOUND_RESULT)
            )
        )

    def ditmenavi_load(self):
        res = requests.get('https://queue.ditmenavi.com', timeout=2)
        content = res.content.decode()
        soup = BeautifulSoup(content, 'html.parser')
        rows = soup.find_all('tr')
        rows = list(rows[1:])
        self.ditmenavi_api = []
        for row in rows:
            data = row.find_all('td')
            raw = {
                'timestamp' : data[1].text,
                'name' : data[2].text,
                'content' : data[3].text,
                'category' : data[4].text,
            }
            # 2024-10-11 14:18:08
            date_format = '%Y-%m-%d %H:%M:%S'
            raw['timestamp'] = datetime.strptime(raw['timestamp'], date_format)

            self.ditmenavi_api.append(raw)

    @commands.command(name='ditmenavi')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ditmenavi(self, ctx:commands.Context):
        ct = random.choice(self.ditmenavi_api)
        embed = discord.Embed(colour=discord.Color.random(),
                              description=ct['content'],
                              timestamp=ct['timestamp'])
        embed.set_author(name=f"DMNAVI | {ct['category']}' if ct['category']!='' else 'DMNAVI', url='https://ditmenavi.com")
        embed.set_footer(text=ct['name'])
        await ctx.send(embed=embed)
    
    @commands.command(name='number')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def number(self, ctx: commands.Context, number: int = None):
        """Get a random fact about a number from numbersapi.com"""
        url = f'http://numbersapi.com/{number if number else "random"}/trivia'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    fact = await resp.text()
                    embed = discord.Embed(
                        title=f"Number Fact: {number if number else 'Random'}",
                        description=fact,
                        color=discord.Color.blue()
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Cá mập cắn cáp oooooooo")
    @commands.command(name='qr')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def qr(self, ctx: commands.Context, *, txt:str = None):
        if txt == None: return
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(txt)}')
        await ctx.reply(embed=embed, mention_author=False)