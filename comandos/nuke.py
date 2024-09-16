import discord
from discord.ext import commands
from discord import app_commands

NUKE_EMOJI = "💥"
SUCCESS_EMOJI = "✅"
FAIL_EMOJI = "❌"


def setup_nuke(bot):
    async def execute_nuke(channel, author):
        channel_name = channel.name
        channel_category = channel.category
        channel_position = channel.position
        channel_permissions = channel.overwrites

        embed = discord.Embed(
            title=f"{NUKE_EMOJI} Canal Nukado!",
            description=f"O canal **{channel_name}** foi destruído e reconstruído.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Nukado por {author}", icon_url=author.avatar.url)

        try:
            new_channel = await channel.clone(
                name=channel_name,
                reason=f"Nuke command triggered by {author}"
            )
            await channel.delete(reason=f"Nuke command triggered by {author}")
            await new_channel.edit(category=channel_category, position=channel_position, overwrites=channel_permissions)
            await new_channel.send(embed=embed)
        except Exception as e:
            return f"{FAIL_EMOJI} **Falha ao nukar o canal!** Erro: {e}"

        return None


    # Comando usando bot.command
    @bot.command(name="nuke")
    @commands.has_permissions(administrator=True)
    async def nuke(ctx, channel_id: int = None):
        channel = ctx.guild.get_channel(channel_id) if channel_id else ctx.channel
        if not channel:
            await ctx.send(f"{FAIL_EMOJI} **Canal não encontrado!**")
            return

        error = await execute_nuke(channel, ctx.author)
        if error:
            await ctx.send(error)


    # Comando usando bot.tree.command (slash command)
    @bot.tree.command(name="nuke", description="Exclui e recria o canal com as mesmas configurações.")
    @app_commands.checks.has_permissions(administrator=True)
    async def nuke_slash(interaction: discord.Interaction, channel_id: int = None):
        channel = interaction.guild.get_channel(channel_id) if channel_id else interaction.channel
        if not channel:
            await interaction.response.send_message(f"{FAIL_EMOJI} **Canal não encontrado!**", ephemeral=True)
            return

        error = await execute_nuke(channel, interaction.user)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
        else:
            await interaction.response.send_message(f"{NUKE_EMOJI} Canal nukado com sucesso!", ephemeral=True)