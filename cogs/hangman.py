import discord
import random
from discord.ext import commands, tasks
from discord_buttons_plugin import *
import threading
import asyncio
import time
import json

buttons = None
games = []

def generate_embed(text):
    return discord.Embed(color=0xff0000, description=text)

async def parse_message(text, json):
    
    if text.lower().startswith('>') and len(text) > 1:
        if json['word'] == ' '.join(text[1:].split()):
            await json['channel'].send('¡Correcto!')
            
            for i in ''.join(text[1:].split()):
                if i not in json['letters']:
                    json['letters'].append(i)
        else:
            await json['channel'].send('Incorrecto')
            switch_turn(json)
    
    elif len(text) != 1 or text in json['letters']:
        await json['channel'].send("Repetida")
        return False
    
    else:
        if text in json['word']:
            await json['channel'].send('Yup')
        else:
            await json['channel'].send('Nope')
            switch_turn(json)
        
        json['letters'].append(text)
    await json['channel'].send(embed=generate_embed(await generate_hangman_message(json)))
    return True

def find_json(user, sub=''):
    for i in games:
        for key in i:
            if i[key] == user or (key != 'author' and i[key] == sub):
                return i

        #if i['player1'] == user or i['']or i['player2'] == user or i['author'] == user:
        #    return i
    return ''

async def generate_hangman_message(json):
    s = f"<@{json['player' + str(json['turn'])]}>\nLetras: {', '.join(json['letters'])}\nTiempo: 30seg\n\n**"
    count = 0
    
    for i in json['word']:
        if i in json['letters']:
            s += str(i).upper()
            count += 1
        elif i == ' ':
            s += '\n'
            count += 1
        else:
            s += "🔵"
    
    if count == len(json['word']):
        s += f"**\n**¡Palabra adivinada!**\nGanador: <@{json['player' + str(json['turn'])]}>"
        games.remove(json)
        
        for i in json['messages']:
            await i.edit(
                embed=generate_embed(i.embeds[0].description + f"\n<@{json['player' + str(json['turn'])]}> ¡Ganó!"))
    else:
        s += "**\n\nUsa `>palabra` si ya la conoces\n"
    return s

async def hangman_command(ctx, user1, user2, channel):

    if find_json(user1.id, user2.id) != '':
        await ctx.send('¡Un juego con uno de estos jugadores ya existe!')
        return

    word = ' '.join(ctx.message.content.split()[4:])

    j = {
        'author': ctx.author.id,
        'player1': user1.id,
        'player2': user2.id,
        'turn': random.randint(0, 1),
        'channel': channel,
        'word': word.lower(),
        'letters': [],
        'id': len(games)
    }

    message = await ctx.send(
        embed=generate_embed(f'<@{user1.id}> & <@{user2.id}>\nPalabra: {word}'),
        )
    '''
    await buttons.send(
        content='',
        channel=ctx.channel.id,
        components=[
            ActionRow([
                Button(
                    label='Stop Game',
                    style=ButtonType().Danger,
                    custom_id='stop_game'
                    )
                ])
            ]
        )'''
    j['messages'] = [message]
    games.append(j)
    j['messages'].append(await channel.send(embed=generate_embed(f'Bienvenido al Ahorcado\n<@{user1.id}> vs <@{user2.id}>')))

def switch_turn(json):
    if json['turn'] == 1:
        json['turn'] = 2
    else:
        json['turn'] = 1

class Hangman(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        #buttons = ButtonsClient(self.bot)

    @commands.Cog.listener()
    async def on_ready(self):
        print('hangman cod loaded.')

    @commands.command()
    async def hangman(self, ctx, user1:discord.User, user2:discord.User, channel:discord.TextChannel):
        await hangman_command(ctx, user1, user2, channel)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.id == self.bot.user.id and len(message.embeds) == 1 and message.embeds[0].description.startswith(
                'Bienvenido al Ahorcado'):
            time.sleep(2)
            game = {}

            for game in games:
                if message in game['messages']:
                    break

            await message.channel.send(embed=generate_embed(await generate_hangman_message(game)))

            def check(mes):
                return game['player' + str(game['turn'])] == mes.author.id and mes.channel == game['channel']

            def json_check(j):
                return j in games

            while json_check(game):
                try:
                    m = await self.bot.wait_for('message', check=check, timeout=30)
                    if json_check(game):
                        await parse_message(m.content.lower(), game)
                except asyncio.TimeoutError:
                    switch_turn(game)
                    if json_check(game):
                        await game['channel'].send(f'Se quedó sin tiempo! Ahora es turno de <@{game["player" + str(game["turn"])]}>')

    '''@buttons.click
    async def stop_game(self, interaction):
        
        json = find_json(interaction.member.id)

        if json != '':
            if interaction.member.id == json['author']:
                self.games.remove(json)
                await interaction.message.delete()
                await interaction.channel.send('Game has been stopped')
    '''

async def setup(bot):
    await bot.add_cog(Hangman(bot))