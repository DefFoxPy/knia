import requests
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

class Respuesta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.RESPUESTAS_ID = 1008081974335901777
        self.ROL = 1008083796987482323

    @commands.Cog.listener()
    async def on_ready(self):
        print('Respuesta cod loaded.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Comando en cooldown, intenta en: {round(error.retry_after, 2)} segundos", delete_after = 10)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def updateCanal(self, ctx, id:int):
        self.RESPUESTAS_ID = id
        await ctx.reply('ID del canal de respuesta actualizado')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def updateRol(self, ctx, id:int):
        self.ROL = id
        await ctx.reply('ID del rol actualizado')

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def respuesta(self, ctx, *, mensaje:str):
        # informacion del emisor del mensaje
        member = ctx.author
        name  = member.display_name
        pfp = member.display_avatar

        try:
            await ctx.message.delete()
        except:
            await ctx.send('No tengo permisos para eliminar un mensaje')
            return

        for rol in member.roles:
            if rol.id == self.ROL:
                #creacion del embed con los datos del mensaje
                embed = discord.Embed(
                    title='respuesta',
                    description = mensaje,
                    color = discord.Color.red())
                embed.set_author(name=f'{name}')
                embed.set_thumbnail(url=f'{member.display_avatar}')
                embed.add_field(name='tag', value=member.mention)

                try:
                    channel = self.bot.get_channel(self.RESPUESTAS_ID)
                    await channel.send(embed=embed)
                    await ctx.send(f'Su respuesta ha sido registrada {member.mention}')
                    return
                except:
                    await ctx.send(f'No tengo acceso al canal {self.RESPUESTAS_ID} o no existe')
            
        await ctx.send(f'No cuentas con el rol de eventos para participar {member.mention}')
  
async def setup(bot):
    await bot.add_cog(Respuesta(bot))