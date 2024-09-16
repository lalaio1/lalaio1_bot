import discord
from discord.ext import commands
from discord import app_commands

def setup_fake(bot):
    @bot.command(name="fake", help="Muda o apelido para um nome falso.")
    @commands.has_permissions(manage_nicknames=True)
    async def fake(ctx, member: discord.Member = None, *, novo_apelido: str):
        member = member or ctx.author
        try:
            await member.edit(nick=novo_apelido)
            embed = discord.Embed(
                title="🔄 Apelido Alterado",
                description=f"O apelido de **{member.display_name}** foi alterado para **{novo_apelido}**!",
                color=discord.Color.blue()  # Usei blue no lugar de cyan
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não consegui alterar o apelido. Verifique minhas permissões.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @bot.tree.command(name="fake", description="Muda o apelido de um usuário para um nome falso.")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def fake(interaction: discord.Interaction, member: discord.Member = None, novo_apelido: str = None):
        member = member or interaction.user
        try:
            await member.edit(nick=novo_apelido)
            embed = discord.Embed(
                title="🔄 Apelido Alterado",
                description=f"O apelido de **{member.display_name}** foi alterado para **{novo_apelido}**!",
                color=discord.Color.blue()  # Usei blue no lugar de cyan
            )
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não consegui alterar o apelido. Verifique minhas permissões.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @fake.error
    async def fake_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                "❌ Você não tem permissão para alterar apelidos.",
                ephemeral=True
            )
