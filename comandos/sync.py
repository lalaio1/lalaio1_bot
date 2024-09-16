import discord
from discord.ext import commands

def setup_sync(bot):
    @bot.tree.command(name='sync', description='Sincroniza os comandos com o Discord.')
    @commands.is_owner()
    async def sync(interaction: discord.Interaction):
        try:
            # Sincronizar comandos com o Discord
            await bot.tree.sync()
            await interaction.response.send_message(embed=discord.Embed(description="🔄 Comandos sincronizados com sucesso!", color=discord.Color.green()), ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(embed=discord.Embed(description=f"❌ Ocorreu um erro ao sincronizar os comandos: {str(e)}", color=discord.Color.red()), ephemeral=True)