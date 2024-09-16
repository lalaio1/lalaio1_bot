import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta
import asyncio

def setup_moverinf(bot):
    @bot.command()
    async def moverinf(ctx, member: discord.Member, seconds: int):
        try:
            if not ctx.author.guild_permissions.move_members:
                embed = discord.Embed(
                    title="🚫 Permissão Insuficiente",
                    description="Você não tem permissão para mover membros.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            if member.id == 1169781984927686696:
                embed = discord.Embed(
                    title="⚠️ Ação Não Permitida",
                    description="Você não pode mover este membro específico.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            voice_channels = [vc for vc in ctx.guild.voice_channels if vc.permissions_for(ctx.guild.me).connect]
            if len(voice_channels) < 2:
                embed = discord.Embed(
                    title="❌ Canais Insuficientes",
                    description="Não há canais de voz suficientes para mover o membro.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            if seconds <= 0:
                embed = discord.Embed(
                    title="⏲️ Tempo Inválido",
                    description="O tempo deve ser um número positivo de segundos.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            if member.voice is None or member.voice.channel is None:
                embed = discord.Embed(
                    title="🚫 Membro Ausente",
                    description="O membro não está em um canal de voz.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            embed_start = discord.Embed(
                title="🚀 Mover Membro Iniciado!",
                description=f"O membro {member.mention} será movido entre canais de voz por **{seconds} segundos**.",
                color=discord.Color.gold()
            )
            embed_start.set_thumbnail(url="https://i.ibb.co/6Rj5gGR/moving.png")  # URL da imagem de início
            await ctx.send(embed=embed_start)

            start_channel = member.voice.channel  # Canal de voz inicial do membro
            end_time = datetime.utcnow() + timedelta(seconds=seconds)

            while datetime.utcnow() < end_time:
                if member.voice and member.voice.channel:
                    current_channel = member.voice.channel
                    available_channels = [vc for vc in voice_channels if vc != current_channel]

                    if available_channels:
                        new_channel = random.choice(available_channels)
                        try:
                            await member.move_to(new_channel)
                            print(f"Moved {member} to {new_channel.name}")  # Apenas para registro
                        except discord.Forbidden:
                            embed_error = discord.Embed(
                                title="🚫 Erro ao Mover Membro",
                                description="Não tenho permissão para mover o membro.",
                                color=discord.Color.red()
                            )
                            await ctx.send(embed=embed_error)
                            return
                        except discord.HTTPException as e:
                            embed_error = discord.Embed(
                                title="🚫 Erro ao Mover Membro",
                                description=f"Ocorreu um erro ao tentar mover o membro: {e}",
                                color=discord.Color.red()
                            )
                            await ctx.send(embed=embed_error)
                            return
                        await asyncio.sleep(0.1)
                    else:
                        embed_error = discord.Embed(
                            title="🚫 Canais Indisponíveis",
                            description="Não há canais disponíveis para mover o membro.",
                            color=discord.Color.red()
                        )
                        await ctx.send(embed=embed_error)
                        break
                else:
                    await asyncio.sleep(0.1)  
          
            try:
                if member.voice and member.voice.channel:  
                    await member.move_to(start_channel)
                    print(f"Moved {member} back to {start_channel.name}") 
            except discord.Forbidden:
                embed_error = discord.Embed(
                    title="🚫 Erro ao Mover Membro",
                    description="Não tenho permissão para mover o membro de volta ao canal inicial.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed_error)
            except discord.HTTPException as e:
                embed_error = discord.Embed(
                    title="🚫 Erro ao Mover Membro",
                    description=f"Ocorreu um erro ao tentar mover o membro de volta: {e}",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed_error)

            embed_end = discord.Embed(
                title="✅ Mover Membro Concluído!",
                description=f"A movimentação de {member.mention} foi concluída.",
                color=discord.Color.green()
            )
            embed_end.set_thumbnail(url="https://i.ibb.co/2sS0JG0/completed.png")  # URL da imagem de conclusão
            await ctx.send(embed=embed_end)

        except Exception as e:
            embed_error = discord.Embed(
                title="🚨 Erro Inesperado",
                description=f"Ocorreu um erro inesperado: {e}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed_error)