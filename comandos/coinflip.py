import discord
import random
from discord.ext import commands
from random import choice

def setup_coinflip(bot):
    @bot.command(name='coinflip', help='Simula o lançamento de uma moeda.')
    async def coin_flip(ctx):
        try:
            result = random.choice(['Cara', 'Coroa'])
            
            embed = discord.Embed(
                title="🪙 Lançamento de Moeda",
                description=f"Resultado: **{result}**",
                color=discord.Color.gold()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await ctx.reply(embed=embed)
        
        except Exception as e:
            await ctx.reply(f"🚫 Erro ao lançar moeda: {str(e)}")


    @bot.tree.command(name='coinflip', description='Lance uma moeda e veja se cai cara ou coroa!')
    async def coin_flip(interaction: discord.Interaction):
        try:
            result = choice(['Cara', 'Coroa'])

            embed = discord.Embed(
                title="🪙 Lançamento de Moeda",
                description=f"Resultado: **{result}**",
                color=discord.Color.gold()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")

            await interaction.response.send_message(embed=embed)  # Use interaction.response.send_message

        except Exception as e:
            await interaction.response.send_message(f" Erro ao lançar moeda: {str(e)}", ephemeral=True)
