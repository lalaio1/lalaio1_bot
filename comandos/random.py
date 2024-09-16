import discord
from discord.ext import commands
import random

def setup_random(bot):
    @bot.command(name='random', help='Gera um número aleatório dentro de um intervalo. Uso: L.random <início> <fim>')
    async def generate_random_number(ctx, start: str, end: str = None):
        try:
            if not start.isdigit():
                raise commands.BadArgument("Certifique-se de fornecer um número inteiro válido para o início.")

            start = int(start)

            if end is None:
                raise commands.BadArgument("Falta o argumento para o fim. Certifique-se de fornecer ambos os números de início e fim.")

            if not end.isdigit():
                raise commands.BadArgument("Certifique-se de fornecer um número inteiro válido para o fim.")

            end = int(end)

            if start >= end:
                raise commands.BadArgument("O valor de início deve ser menor que o valor de fim.")
            
            random_number = random.randint(start, end)
            
            embed = discord.Embed(
                title="🎲 Número Aleatório",
                description=f"O número aleatório gerado entre {start} e {end} é: **{random_number}**",
                color=discord.Color.orange()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await ctx.reply(embed=embed)
        
        except commands.BadArgument as e:
            embed = discord.Embed(
                title="🚫 Erro ao Gerar Número Aleatório",
                description=str(e),
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        
        except ValueError:
            embed = discord.Embed(
                title="🚫 Erro ao Gerar Número Aleatório",
                description="Certifique-se de fornecer números inteiros válidos como início e fim.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        
        except Exception as e:
            embed = discord.Embed(
                title="🚫 Erro",
                description=f"Ocorreu um erro inesperado: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)

    @bot.tree.command(name='random', description='Gera um número aleatório dentro de um intervalo.')
    async def generate_random_number(interaction: discord.Interaction, start: int, end: int):
        try:
            if start >= end:
                await interaction.response.send_message("O valor de início deve ser menor que o valor de fim.", ephemeral=True)
                return
            
            random_number = random.randint(start, end)
            
            embed = discord.Embed(
                title="🎲 Número Aleatório",
                description=f"O número aleatório gerado entre {start} e {end} é: **{random_number}**",
                color=discord.Color.orange()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            embed = discord.Embed(
                title="🚫 Erro",
                description=f"Ocorreu um erro inesperado: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)