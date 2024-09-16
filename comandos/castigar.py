import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

def setup_castigar(bot):
    @bot.command(name='castigar', help='Aplica um castigo a um membro do servidor')
    @commands.has_permissions(moderate_members=True)
    async def castigar(ctx, membro: discord.Member, duration: int, *, motivo: str = None):
        if membro == ctx.author:
            embed = discord.Embed(
                title='❌ Operação Inválida',
                description="Você não pode se castigar a si mesmo.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return
        elif membro == bot.user:
            embed = discord.Embed(
                title='❌ Operação Inválida',
                description="Eu não posso me castigar.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        try:
            # Aplicar o castigo (timeout) ao membro
            until_time = discord.utils.utcnow() + timedelta(seconds=duration)
            await membro.edit(timed_out_until=until_time, reason=motivo)

            embed = discord.Embed(
                title=f'⚠️ {membro} foi castigado',
                description=f'Usuário ID: {membro.id}\nDuração: {duration} segundos',
                color=discord.Color.orange()
            )

            if motivo:
                embed.add_field(name='📜 Motivo', value=motivo, inline=False)

            embed.set_thumbnail(url=membro.avatar.url)
            embed.set_footer(text=f'Castigado por {ctx.author}', icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed)

            dm_embed = discord.Embed(
                title='⚠️ Você foi castigado',
                description=f'Você foi castigado no servidor **{ctx.guild.name}** por {duration} segundos.',
                color=discord.Color.orange()
            )

            if motivo:
                dm_embed.add_field(name='📜 Motivo', value=motivo, inline=False)

            dm_embed.add_field(name='🆔 ID do Usuário', value=membro.id, inline=False)
            dm_embed.set_thumbnail(url=ctx.guild.icon.url)
            dm_embed.set_footer(text=f'Castigado por {ctx.author}', icon_url=ctx.author.avatar.url)

            await membro.send(embed=dm_embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para castigar membros neste servidor.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title='❌ Erro ao Castigar',
                description=f"Ocorreu um erro ao tentar castigar {membro}. Por favor, tente novamente mais tarde.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro Inesperado',
                description=f"Ocorreu um erro inesperado ao tentar castigar {membro}: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)

    @bot.tree.command(name='castigar', description='Aplica um castigo a um membro')
    @app_commands.checks.has_permissions(moderate_members=True)
    async def castigar_slash(interaction: discord.Interaction, membro: discord.Member, duration: int, motivo: str = None):
        if interaction.response.is_done():
            return
        
        if membro == interaction.user:
            embed = discord.Embed(
                title='❌ Operação Inválida',
                description="Você não pode se castigar a si mesmo.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        elif membro == bot.user:
            embed = discord.Embed(
                title='❌ Operação Inválida',
                description="Eu não posso me castigar.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            # Aplicar o castigo (timeout) ao membro
            until_time = discord.utils.utcnow() + timedelta(seconds=duration)
            await membro.edit(timed_out_until=until_time, reason=motivo)

            embed = discord.Embed(
                title=f'⚠️ {membro} foi castigado',
                description=f'Usuário ID: {membro.id}\nDuração: {duration} segundos',
                color=discord.Color.orange()
            )

            if motivo:
                embed.add_field(name='📜 Motivo', value=motivo, inline=False)

            embed.set_thumbnail(url=membro.avatar.url)
            embed.set_footer(text=f'Castigado por {interaction.user}', icon_url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)

            dm_embed = discord.Embed(
                title='⚠️ Você foi castigado',
                description=f'Você foi castigado no servidor **{interaction.guild.name}** por {duration} segundos.',
                color=discord.Color.orange()
            )

            if motivo:
                dm_embed.add_field(name='📜 Motivo', value=motivo, inline=False)

            dm_embed.add_field(name='🆔 ID do Usuário', value=membro.id, inline=False)
            dm_embed.set_thumbnail(url=interaction.guild.icon.url)
            dm_embed.set_footer(text=f'Castigado por {interaction.user}', icon_url=interaction.user.avatar.url)

            await membro.send(embed=dm_embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para castigar membros neste servidor.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title='❌ Erro ao Castigar',
                description=f"Ocorreu um erro ao tentar castigar {membro}. Por favor, tente novamente mais tarde.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro Inesperado',
                description=f"Ocorreu um erro inesperado ao tentar castigar {membro}: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @bot.command(name='removercastigo', help='Remove o castigo de um membro do servidor')
    @commands.has_permissions(moderate_members=True)
    async def removercastigo(ctx, membro_id: int):
        try:
            membro = await ctx.guild.fetch_member(membro_id)
            if not membro.timed_out_until:
                embed = discord.Embed(
                    title='❌ Operação Inválida',
                    description="Este membro não está castigado.",
                    color=discord.Color.red()
                )
                await ctx.reply(embed=embed)
                return

            await membro.edit(timed_out_until=None)

            embed = discord.Embed(
                title=f'⚠️ Castigo removido',
                description=f'Usuário {membro} (ID: {membro.id}) teve seu castigo removido.',
                color=discord.Color.green()
            )

            embed.set_thumbnail(url=membro.avatar.url)
            embed.set_footer(text=f'Removido por {ctx.author}', icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed)

            dm_embed = discord.Embed(
                title='⚠️ Seu castigo foi removido',
                description=f'Seu castigo no servidor **{ctx.guild.name}** foi removido.',
                color=discord.Color.green()
            )

            dm_embed.set_thumbnail(url=ctx.guild.icon.url)
            dm_embed.set_footer(text=f'Removido por {ctx.author}', icon_url=ctx.author.avatar.url)

            await membro.send(embed=dm_embed)

        except discord.NotFound:
            embed = discord.Embed(
                title='❌ Membro não encontrado',
                description=f"Não foi possível encontrar um membro com o ID {membro_id}.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para remover o castigo deste membro.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title='❌ Erro ao Remover Castigo',
                description=f"Ocorreu um erro ao tentar remover o castigo do membro. Por favor, tente novamente mais tarde.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro Inesperado',
                description=f"Ocorreu um erro inesperado ao tentar remover o castigo do membro: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)

    @bot.tree.command(name='removercastigo', description='Remove o castigo de um membro')
    @app_commands.checks.has_permissions(moderate_members=True)
    async def removercastigo_slash(interaction: discord.Interaction, membro: discord.Member):
        try:
            if not membro.timed_out_until:
                embed = discord.Embed(
                    title='❌ Operação Inválida',
                    description="Este membro não está castigado.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            await membro.edit(timed_out_until=None)

            embed = discord.Embed(
                title=f'⚠️ Castigo removido',
                description=f'Usuário {membro} (ID: {membro.id}) teve seu castigo removido.',
                color=discord.Color.green()
            )

            embed.set_thumbnail(url=membro.avatar.url)
            embed.set_footer(text=f'Removido por {interaction.user}', icon_url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)

            dm_embed = discord.Embed(
                title='⚠️ Seu castigo foi removido',
                description=f'Seu castigo no servidor **{interaction.guild.name}** foi removido.',
                color=discord.Color.green()
            )

            dm_embed.set_thumbnail(url=interaction.guild.icon.url)
            dm_embed.set_footer(text=f'Removido por {interaction.user}', icon_url=interaction.user.avatar.url)

            await membro.send(embed=dm_embed)

        except discord.NotFound:
            embed = discord.Embed(
                title='❌ Membro não encontrado',
                description=f"Não foi possível encontrar o membro mencionado.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para remover o castigo deste membro.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title='❌ Erro ao Remover Castigo',
                description=f"Ocorreu um erro ao tentar remover o castigo do membro. Por favor, tente novamente mais tarde.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro Inesperado',
                description=f"Ocorreu um erro inesperado ao tentar remover o castigo do membro: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)