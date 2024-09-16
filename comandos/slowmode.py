import discord
from discord.ext import commands
from discord import app_commands

def setup_slowmode(bot):
    async def set_slowmode(ctx_or_interaction, seconds: int):
        try:
            if seconds < 0:
                raise ValueError("O tempo de slowmode deve ser um valor não negativo.")

            await ctx_or_interaction.channel.edit(slowmode_delay=seconds)

            if seconds == 0:
                title = "🚫 Modo Lento Desativado!"
                description = "Você pode agora enviar mensagens sem esperar entre elas!"
                thumbnail_url = "https://i.ibb.co/px3VhWn/disable.png"
            else:
                title = "🕒 Slowmode Atualizado!"
                description = f"O tempo de slowmode foi atualizado para {seconds} segundos."
                thumbnail_url = "https://i.ibb.co/kKZ3w96/clock.png"

            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=thumbnail_url)
            if isinstance(ctx_or_interaction, commands.Context):
                await ctx_or_interaction.reply(embed=embed)
            else:
                await ctx_or_interaction.response.send_message(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="⚠️ Permissão Negada!",
                description="Eu não tenho permissão para editar este canal.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://i.ibb.co/Wf0vPdP/error.png")
            if isinstance(ctx_or_interaction, commands.Context):
                await ctx_or_interaction.reply(embed=embed)
            else:
                await ctx_or_interaction.response.send_message(embed=embed)

        except ValueError as e:
            embed = discord.Embed(
                title="⚠️ Tempo de Slowmode Inválido!",
                description=str(e),
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://i.ibb.co/Wf0vPdP/error.png")
            if isinstance(ctx_or_interaction, commands.Context):
                await ctx_or_interaction.reply(embed=embed)
            else:
                await ctx_or_interaction.response.send_message(embed=embed)

        except discord.HTTPException as e:
            embed = discord.Embed(
                title="⚠️ Ocorreu um Erro!",
                description=f"Ocorreu um erro ao tentar atualizar o slowmode.\nDetalhes do erro: `{e}`",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://i.ibb.co/Wf0vPdP/error.png")
            if isinstance(ctx_or_interaction, commands.Context):
                await ctx_or_interaction.reply(embed=embed)
            else:
                await ctx_or_interaction.response.send_message(embed=embed)

    @bot.command(name='slowmode', help='Configura o tempo de slowmode em segundos. Uso: A.slowmode <segundos>')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(ctx, seconds: int = None):
        if seconds is None:
            embed = discord.Embed(
                title="⚠️ Tempo de Slowmode Inválido!",
                description="Por favor, forneça um valor em segundos para o tempo de slowmode.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://i.ibb.co/Wf0vPdP/error.png")
            await ctx.reply(embed=embed)
            return

        await set_slowmode(ctx, seconds)

    @bot.command(name='unslowmode', help='Desativa o modo lento do canal. Uso: A.unslowmode')
    @commands.has_permissions(manage_channels=True)
    async def unslowmode(ctx):
        await set_slowmode(ctx, seconds=0)

    @slowmode.error
    @unslowmode.error
    async def slowmode_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="⚠️ Permissão Negada!",
                description="Você não tem permissão para usar este comando.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://i.ibb.co/Wf0vPdP/error.png")
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="⚠️ Ocorreu um Erro!",
                description=f"Ocorreu um erro inesperado.\nDetalhes do erro: `{error}`",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://i.ibb.co/Wf0vPdP/error.png")
            await ctx.reply(embed=embed)

    @bot.tree.command(name='slowmode', description='Configura o tempo de slowmode em segundos. Uso: /slowmode <segundos>')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(interaction: discord.Interaction, seconds: int = None):
        if seconds is None:
            embed = discord.Embed(
                title="⚠️ Tempo de Slowmode Inválido!",
                description="Por favor, forneça um valor em segundos para o tempo de slowmode.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://i.ibb.co/Wf0vPdP/error.png")
            await interaction.response.send_message(embed=embed)
            return

        await set_slowmode(interaction, seconds)

    @bot.tree.command(name='unslowmode', description='Desativa o modo lento do canal. Uso: /unslowmode')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unslowmode(interaction: discord.Interaction):
        await set_slowmode(interaction, seconds=0)

    @slowmode.error
    @unslowmode.error
    async def slowmode_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            embed = discord.Embed(
                title="⚠️ Permissão Negada!",
                description="Você não tem permissão para usar este comando.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://i.ibb.co/Wf0vPdP/error.png")
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="⚠️ Ocorreu um Erro!",
                description=f"Ocorreu um erro inesperado.\nDetalhes do erro: `{error}`",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://i.ibb.co/Wf0vPdP/error.png")
            await interaction.response.send_message(embed=embed)
