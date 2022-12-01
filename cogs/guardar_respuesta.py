import discord
from discord import app_commands
from discord.ext import commands

SERVER_ID = 876137221462319124 #1009259025994633326

class Respuesta(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.RESPUESTAS_ID = 1047972181247795374
        self.ROL = 1047972305097195649

    @commands.Cog.listener()
    async def on_ready(self):
        print('Respuesta cod loaded.')
    '''
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Comando en cooldown, intenta en: {round(error.retry_after, 2)} segundos")#, delete_after = 10)
    '''

    @app_commands.command(name='updatecanal', description='modifica la id del canal donde será enviado el mensaje del bot')
    async def updatecanal(self, interaction: discord.Interaction, id_canal: str):
        if id_canal.isdigit():
            self.RESPUESTAS_ID = int(id_canal)
            await interaction.response.send_message('La ID del canal de respuesta se ha actualizado.')
        else:
            await interaction.response.send_message('La ID enviada no está conformada por digitos, intente de nuevo.')

    @app_commands.command(name='updaterol', description='modifica la id del rol el cual se usa para indicar quienes son los participantes del evento')
    async def updaterol(self, interaction: discord.Interaction, id_rol: str):
        if id_rol.isdigit():
            self.ROL = int(id_rol)
            await interaction.response.send_message('Se modificado cual será el rol del evento')
        else:
            await interaction.response.send_message('La ID enviada no está conformada por digitos, intente de nuevo.')

    @app_commands.command(name='respuesta', description='Envia un texto a un canal selecionado para recibir respuesta de usuarios en un evento')
    #@app_commands.checks.cooldown(1, 7200, key=lambda i: (i.guild_id, i.user.id))
    async def respuesta(self, interaction: discord.Interaction, answer: str):
        user = interaction.user
        
        for rol in user.roles:
            if rol.id == self.ROL: # se ha confirmado que el usuario tiene el rol de eventos
                embed = discord.Embed(
                    title='respuesta',
                    description=answer,
                    color=discord.Color.red()
                )
                embed.set_author(name=f'{user.display_name}')
                embed.set_thumbnail(url=f'{user.display_avatar}')
                embed.add_field(name='tag', value=user.mention)

                try:
                    channel = self.bot.get_channel(self.RESPUESTAS_ID)
                    await channel.send(embed=embed)
                    await interaction.response.send_message(f'{user.mention} tu respuesta del evento será revisada por un staff ahora mismo!')
                except:
                    await interaction.response.send_message(f'No tengo acceso al canal {self.RESPUESTAS_ID} o no existe')
                return

        await interaction.response.send_message('No cuentas con el rol de eventos para poder enviar tu respuesta')







async def setup(bot):
    await bot.add_cog(Respuesta(bot), guilds = [discord.Object(id = SERVER_ID)])
