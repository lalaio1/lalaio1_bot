import discord
import requests
from bs4 import BeautifulSoup

def setup_wiki(bot):
    @bot.command(name='wiki', help='Pesquisa um termo na Wikipedia')
    async def wiki(ctx, *, termo):
        termo_formatado = termo.replace(' ', '_')
        pesquisa = f"https://pt.wikipedia.org/wiki/{termo_formatado}"
        
        try:
            response = requests.get(pesquisa)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')
            resumo = soup.find('div', class_='mw-parser-output').find('p').text.strip()
            embed = discord.Embed(title=f"Resultado da pesquisa: {termo}", url=pesquisa, color=discord.Color.blue())
            embed.add_field(name="Link para a Wikipedia:", value=f"[{termo}](https://pt.wikipedia.org/wiki/{termo_formatado})", inline=False)
            embed.add_field(name="Resumo:", value=resumo[:500] + '...' if len(resumo) > 500 else resumo, inline=False)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Wikipedia-logo.png/600px-Wikipedia-logo.png")

            await ctx.reply(embed=embed)

        except requests.HTTPError:
            embed = discord.Embed(title=f"Resultado da pesquisa: {termo}", description="Não foi possível encontrar informações na Wikipedia para este termo.", color=discord.Color.red())
            await ctx.reply(embed=embed)

        except Exception as e:
            embed = discord.Embed(title=f"Erro ao pesquisar: {termo}", description=f"Ocorreu um erro durante a pesquisa: {str(e)}", color=discord.Color.red())
            await ctx.reply(embed=embed)

    @bot.tree.command(name='wiki', description='Pesquisa um termo na Wikipedia')
    async def wiki(interaction: discord.Interaction, termo: str):
        termo_formatado = termo.replace(' ', '_')
        pesquisa = f"https://pt.wikipedia.org/wiki/{termo_formatado}"
        
        try:
            response = requests.get(pesquisa)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            resumo = soup.find('div', class_='mw-parser-output').find('p').text.strip()

            embed = discord.Embed(
                title=f"Resultado da pesquisa: {termo}",
                url=pesquisa,
                color=discord.Color.blue()
            )
            embed.add_field(name="Link para a Wikipedia:", value=f"[{termo}](https://pt.wikipedia.org/wiki/{termo_formatado})", inline=False)
            embed.add_field(name="Resumo:", value=resumo[:500] + '...' if len(resumo) > 500 else resumo, inline=False)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Wikipedia-logo.png/600px-Wikipedia-logo.png")
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await interaction.response.send_message(embed=embed)

        except requests.HTTPError:
            embed = discord.Embed(
                title=f"Resultado da pesquisa: {termo}",
                description="Não foi possível encontrar informações na Wikipedia para este termo.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title=f"Erro ao pesquisar: {termo}",
                description=f"Ocorreu um erro durante a pesquisa: {str(e)}",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)