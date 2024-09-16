import requests
import discord
from discord.ext import commands

def setup_randomname(bot):
    @bot.command(name='randomname', help='Gera um nome aleatório. Uso: A.randomname <tema/idioma>')
    async def random_name(ctx, theme: str):
        try:
            # Verifica se o tema/idioma é válido (por exemplo, apenas 'us' é suportado pelo API randomuser.me)
            valid_themes = ['us', 'au', 'br', 'ca', 'ch', 'de', 'dk', 'es', 'fi', 'fr', 'gb', 'ie', 'ir', 'nl', 'nz', 'tr']
            if theme not in valid_themes:
                raise commands.BadArgument(f"Tema/idioma não suportado. Escolha um dos temas: {', '.join(valid_themes)}")
            
            # Faz a requisição à API randomuser.me para obter o nome aleatório
            response = requests.get(f'https://randomuser.me/api/?nat={theme}')
            response.raise_for_status()  # Lança um erro se a requisição não for bem-sucedida
            
            # Obtém o nome aleatório a partir dos dados da resposta
            name_data = response.json()['results'][0]['name']
            name = f"{name_data['first'].capitalize()} {name_data['last'].capitalize()}"
            
            # Cria um embed para exibir o nome gerado
            embed = discord.Embed(
                title="🎲 Nome Aleatório",
                description=f"**Nome Gerado:** {name}",
                color=discord.Color.green()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            # Envia o embed como resposta
            await ctx.reply(embed=embed)
        
        except commands.BadArgument as e:
            embed = discord.Embed(
                title="🚫 Erro ao Gerar Nome",
                description=str(e),
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        
        except requests.RequestException as e:
            embed = discord.Embed(
                title="🚫 Erro de Requisição",
                description=f"Ocorreu um erro ao tentar acessar a API: {str(e)}",
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

    @bot.tree.command(name='randomname', description='Gera um nome aleatório. inf: theme e o pais, voce pode colocar (exemplo) > br')
    async def random_name(interaction: discord.Interaction, theme: str):
        try:
            valid_themes = ['us', 'au', 'br', 'ca', 'ch', 'de', 'dk', 'es', 'fi', 'fr', 'gb', 'ie', 'ir', 'nl', 'nz', 'tr']
            if theme not in valid_themes:
                await interaction.response.send_message(f"Tema/idioma não suportado. Escolha um dos temas: {', '.join(valid_themes)}", ephemeral=True)
                return
            
            response = requests.get(f'https://randomuser.me/api/?nat={theme}')
            response.raise_for_status()
            
            name_data = response.json()['results'][0]['name']
            name = f"{name_data['first'].capitalize()} {name_data['last'].capitalize()}"
            
            embed = discord.Embed(
                title="🎲 Nome Aleatório",
                description=f"**Nome Gerado:** {name}",
                color=discord.Color.green()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await interaction.response.send_message(embed=embed)
        
        except requests.RequestException as e:
            embed = discord.Embed(
                title="🚫 Erro de Requisição",
                description=f"Ocorreu um erro ao tentar acessar a API: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except Exception as e:
            embed = discord.Embed(
                title="🚫 Erro",
                description=f"Ocorreu um erro inesperado: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)