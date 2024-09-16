import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

def setup_down(bot):
    @bot.command()
    async def down(ctx, *, game_name: str):
        await ctx.message.delete()
        search_url = f'https://www.steamamiga.com/?s={game_name.replace(" ", "+")}'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            await ctx.send("❌ Não foi possível acessar o site. Tente novamente mais tarde.")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Debugging prints
        print("Search URL:", search_url)
        print("Response status code:", response.status_code)

        # Busca o primeiro resultado da pesquisa
        result = soup.find('article')
        if result:
            game_page_url = result.find('a')['href']
            print("Found Game Page URL:", game_page_url)

            # Acessa a página do jogo para obter o link de download
            game_response = requests.get(game_page_url, headers=headers)
            if game_response.status_code != 200:
                await ctx.send("❌ Não foi possível acessar a página do jogo. Tente novamente mais tarde.")
                return

            game_soup = BeautifulSoup(game_response.text, 'html.parser')

            # Debugging prints
            print("Game Page URL:", game_page_url)
            print("Game Page Response status code:", game_response.status_code)

            # Exibir o conteúdo da página do jogo para diagnóstico
            print(game_soup.prettify())

            # Extrai as informações do jogo
            game_title = game_soup.find('h1').text.strip() if game_soup.find('h1') else 'No title'
            game_image = game_soup.find('img')['src'] if game_soup.find('img') else 'No image'
            
            # Tente encontrar o link de download com base em características adicionais
            download_link = game_soup.find('a', href=True, text='Download')  # Ajuste o texto conforme necessário
            if download_link is None:
                # Tente encontrar qualquer link de download potencialmente válido
                possible_download_links = game_soup.find_all('a', href=True)
                for link in possible_download_links:
                    if 'download' in link['href'].lower():
                        download_link = link
                        break

            if download_link:
                download_url = download_link['href']

                # Debugging prints
                print("Download URL:", download_url)
                print("Game Title:", game_title)
                print("Game Image:", game_image)
                
                embed = discord.Embed(title=game_title, url=download_url, color=discord.Color.blue())
                embed.set_thumbnail(url=game_image)
                embed.add_field(name="🔗 Link:", value=f"[Clique aqui para baixar]({download_url})", inline=False)
                
                await ctx.send(embed=embed)
            else:
                print("Download link not found.")
                await ctx.send("❌ Link de download não encontrado. Tente novamente com outro nome.")
        else:
            print("No results found.")
            await ctx.send("❌ Jogo não encontrado. Tente novamente com outro nome.")