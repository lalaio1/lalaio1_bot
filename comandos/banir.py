import discord
from discord.ext import commands
from discord import app_commands

def setup_banir(bot):
    @bot.command(name='ban', help='Bane um membro do servidor pelo membro mencionado ou ID')
    @commands.has_permissions(ban_members=True)
    async def banir(ctx, membro: discord.Member = None, membro_id: int = None, *, motivo: str = None):
        if membro is None and membro_id is None:
            embed = discord.Embed(
                title='❌ Falha na operação',
                description="Você deve fornecer um membro ou ID de usuário.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        if membro is None:
            try:
                membro = await ctx.guild.fetch_member(membro_id)
            except discord.NotFound:
                embed = discord.Embed(
                    title='❌ Usuário não encontrado',
                    description=f'Não foi possível encontrar um membro com o ID {membro_id}.',
                    color=discord.Color.red()
                )
                await ctx.reply(embed=embed)
                return

        if membro == ctx.author:
            embed = discord.Embed(
                title='❌ Operação Inválida',
                description="Você não pode se banir a si mesmo.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return
        elif membro == bot.user:
            embed = discord.Embed(
                title='❌ Operação Inválida',
                description="Eu não posso me banir.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        try:
            await membro.ban(reason=motivo)

            embed = discord.Embed(
                title=f'🔨 {membro} foi banido do servidor',
                color=discord.Color.red()
            )

            if motivo:
                embed.add_field(name='📜 Motivo', value=motivo, inline=False)

            embed.add_field(name='🆔 ID do Usuário', value=membro.id, inline=False)
            embed.set_thumbnail(url=membro.avatar.url)
            embed.set_footer(text=f'Banido por {ctx.author}', icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed)

            dm_embed = discord.Embed(
                title='🔨 Você foi banido',
                description=f'Você foi banido do servidor **{ctx.guild.name}**.',
                color=discord.Color.red()
            )

            if motivo:
                dm_embed.add_field(name='📜 Motivo', value=motivo, inline=False)

            dm_embed.set_thumbnail(url=ctx.guild.icon.url)
            dm_embed.set_footer(text=f'Banido por {ctx.author}', icon_url=ctx.author.avatar.url)

            await membro.send(embed=dm_embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para banir membros neste servidor.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title='❌ Erro ao Banir',
                description=f"Ocorreu um erro ao tentar banir {membro}. Por favor, tente novamente mais tarde.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro Inesperado',
                description=f"Ocorreu um erro inesperado ao tentar banir {membro}: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)

    @bot.tree.command(name='ban', description='Bane um membro do servidor pelo membro mencionado')
    @app_commands.checks.has_permissions(ban_members=True)
    async def banir_slash(interaction: discord.Interaction, membro: discord.Member, motivo: str = None):
        guild = interaction.guild

        if membro == interaction.user:
            embed = discord.Embed(
                title='❌ Operação Inválida',
                description="Você não pode se banir a si mesmo.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        elif membro == interaction.client.user:
            embed = discord.Embed(
                title='❌ Operação Inválida',
                description="Eu não posso me banir.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            # Acknowledge the interaction immediately
            await interaction.response.defer()

            await membro.ban(reason=motivo)

            embed = discord.Embed(
                title=f'🔨 {membro} foi banido do servidor',
                color=discord.Color.red()
            )

            if motivo:
                embed.add_field(name='📜 Motivo', value=motivo, inline=False)

            embed.add_field(name='🆔 ID do Usuário', value=membro.id, inline=False)
            embed.set_thumbnail(url=membro.avatar.url)
            embed.set_footer(text=f'Banido por {interaction.user}', icon_url=interaction.user.avatar.url)

            await interaction.followup.send(embed=embed)

            dm_embed = discord.Embed(
                title='🔨 Você foi banido',
                description=f'Você foi banido do servidor **{interaction.guild.name}**.',
                color=discord.Color.red()
            )

            if motivo:
                dm_embed.add_field(name='📜 Motivo', value=motivo, inline=False)

            dm_embed.set_thumbnail(url=interaction.guild.icon.url)
            dm_embed.set_footer(text=f'Banido por {interaction.user}', icon_url=interaction.user.avatar.url)

            await membro.send(embed=dm_embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para banir membros neste servidor.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException:
            embed = discord.Embed(
                title='❌ Erro ao Banir',
                description=f"Ocorreu um erro ao tentar banir {membro}. Por favor, tente novamente mais tarde.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro Inesperado',
                description=f"Ocorreu um erro inesperado ao tentar banir {membro}: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
    @bot.command(name='unban', help='Desbane um membro do servidor pelo ID')
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, user_id: int):
        try:
            banned_users = await ctx.guild.bans()  # Obtém um gerador de usuários banidos
            
            # Procura o usuário na lista de banidos
            banned_user = None
            async for entry in banned_users:
                if entry.user.id == user_id:
                    banned_user = entry.user
                    break
            
            if banned_user is None:
                embed = discord.Embed(
                    title='❌ Usuário não encontrado',
                    description=f'O usuário com o ID {user_id} não está banido neste servidor.',
                    color=discord.Color.red()
                )
                await ctx.reply(embed=embed)
                return

            await ctx.guild.unban(banned_user)  # Desbanir o usuário

            embed = discord.Embed(
                title=f'✅ {banned_user} foi desbanido do servidor',
                description=f'Usuário ID: {user_id}',
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=banned_user.avatar.url)
            embed.set_footer(text=f'Desbanido por {ctx.author}', icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para desbanir membros neste servidor.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(
                title='❌ Erro ao Desbanir',
                description=f"Ocorreu um erro ao tentar desbanir o usuário com ID {user_id}. Por favor, tente novamente mais tarde.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro Inesperado',
                description=f"Ocorreu um erro inesperado ao tentar desbanir o usuário com ID {user_id}: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)

    @bot.tree.command(name='unban', description='Desbane um membro pelo ID')
    @app_commands.describe(user_id="ID do usuário para desbanir")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban_slash(interaction: discord.Interaction, user_id: str):
        try:
            banned_users = await interaction.guild.bans()  # Obtém um gerador de usuários banidos
            
            # Procura o usuário na lista de banidos
            banned_user = None
            async for entry in banned_users:
                if entry.user.id == int(user_id):
                    banned_user = entry.user
                    break
            
            if banned_user is None:
                embed = discord.Embed(
                    title='❌ Usuário não encontrado',
                    description=f'O usuário com o ID {user_id} não está banido neste servidor.',
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            await interaction.guild.unban(banned_user)  # Desbanir o usuário

            embed = discord.Embed(
                title=f'✅ {banned_user} foi desbanido do servidor',
                description=f'Usuário ID: {user_id}',
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=banned_user.avatar.url)
            embed.set_footer(text=f'Desbanido por {interaction.user}', icon_url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para desbanir membros neste servidor.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException:
            embed = discord.Embed(
                title='❌ Erro ao Desbanir',
                description=f"Ocorreu um erro ao tentar desbanir o usuário com ID {user_id}. Por favor, tente novamente mais tarde.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro Inesperado',
                description=f"Ocorreu um erro inesperado ao tentar desbanir o usuário com ID {user_id}: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)