import discord
from discord.ext import commands

border_color = discord.Color.blue()

def setup_lock(bot):
    @commands.has_permissions(manage_channels=True)
    @bot.command(name='lock', help='Bloqueia o canal para não administradores')
    async def lock(ctx):
        try:
            channel = ctx.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

            embed = discord.Embed(
                title=f"Canal Bloqueado: {channel.name}",
                description=f"O canal {channel.mention} foi bloqueado. Somente administradores podem enviar mensagens agora.",
                color=border_color
            )
            await ctx.reply(embed=embed)

        except discord.Forbidden:
            error_embed = discord.Embed(
                title="Erro ao Bloquear Canal",
                description="Não tenho permissão para alterar permissões neste canal.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Bloquear Canal",
                description=f"Ocorreu um erro ao tentar bloquear o canal: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)

    @lock.error
    async def lock_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error_embed = discord.Embed(
                title="Erro de Permissão",
                description="Você não tem permissão para usar esse comando. (Permissão necessária: Gerenciar Canais)",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)

    @commands.has_permissions(manage_channels=True)
    @bot.command(name='unlock', help='Desbloqueia o canal para todos os membros')
    async def unlock(ctx):
        try:
            channel = ctx.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

            embed = discord.Embed(
                title=f"Canal Desbloqueado: {channel.name}",
                description=f"O canal {channel.mention} foi desbloqueado. Todos os membros podem enviar mensagens novamente.",
                color=border_color
            )
            await ctx.reply(embed=embed)

        except discord.Forbidden:
            error_embed = discord.Embed(
                title="Erro ao Desbloquear Canal",
                description="Não tenho permissão para alterar permissões neste canal.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Desbloquear Canal",
                description=f"Ocorreu um erro ao tentar desbloquear o canal: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)

    @unlock.error
    async def unlock_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error_embed = discord.Embed(
                title="Erro de Permissão",
                description="Você não tem permissão para usar esse comando. (Permissão necessária: Gerenciar Canais)",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)

    @bot.tree.command(name='lock', description='Bloqueia o canal para não administradores.')
    @commands.has_permissions(manage_channels=True)
    async def lock(interaction: discord.Interaction):
        try:
            channel = interaction.channel
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

            embed = discord.Embed(
                title=f"Canal Bloqueado: {channel.name}",
                description=f"O canal {channel.mention} foi bloqueado. Somente administradores podem enviar mensagens agora.",
                color=discord.Color.blue()  # Use sua cor desejada para o borda
            )
            await interaction.response.send_message(embed=embed)

        except discord.Forbidden:
            error_embed = discord.Embed(
                title="Erro ao Bloquear Canal",
                description="Não tenho permissão para alterar permissões neste canal.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Bloquear Canal",
                description=f"Ocorreu um erro ao tentar bloquear o canal: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @bot.tree.command(name='unlock', description='Desbloqueia o canal para todos os membros.')
    @commands.has_permissions(manage_channels=True)
    async def unlock(interaction: discord.Interaction):
        try:
            channel = interaction.channel
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = None
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

            embed = discord.Embed(
                title=f"Canal Desbloqueado: {channel.name}",
                description=f"O canal {channel.mention} foi desbloqueado. Todos os membros podem enviar mensagens novamente.",
                color=discord.Color.blue()  # Use sua cor desejada para o borda
            )
            await interaction.response.send_message(embed=embed)

        except discord.Forbidden:
            error_embed = discord.Embed(
                title="Erro ao Desbloquear Canal",
                description="Não tenho permissão para alterar permissões neste canal.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Desbloquear Canal",
                description=f"Ocorreu um erro ao tentar desbloquear o canal: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)