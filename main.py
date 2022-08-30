import discord
import asyncio
import config
import os

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('z!'), intents=intents, application_id=config.APPLICATION_ID)

@bot.event
async def on_ready():
    print('logged on as', bot.user)

@bot.event
async def on_message(message):
    # Primero procese los eventos
    await bot.process_commands(message) 

    # don't respond to command_prefix
    if message[0:2] == 'z!':
        return

    # don't respond to ourselves
    if message.author == bot.user:
        return
    
    if message.content == 'ping':
        await message.channel.send('Pong.')

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

async def main():
    await load()
    await bot.start(config.TOKEN)

asyncio.run(main())