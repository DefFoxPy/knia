import requests
import discord
from discord.ext import commands

class Numbers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Numbers cod loaded.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def facts(self, ctx, number):
        ''' Usando una API para obtener datos curiosos sobre los números '''
        response = requests.get(f'http://numbersapi.com/{number}')
        embed = discord.Embed(description=response.text)
        await ctx.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Numbers(bot))