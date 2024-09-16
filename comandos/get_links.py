import discord
import requests 
from bs4 import BeautifulSoup
import io




def setup_get_links(bot):
    @bot.command(name='get_links', help='Extrai todos os links de um site. Use !get_links <url>')
    async def get_links(ctx, url):
        processing_embed = discord.Embed(
            title='➿ Processando...',
            description=f'__🔗 Extraindo links do site__ {url}. __Por favor, aguarde.__',
            color=discord.Color.blue()
        )
        processing_message = await ctx.reply(embed=processing_embed)

        if not url.startswith("http://") and not url.startswith("https://"):
            await processing_message.delete()
            await ctx.reply('❌ URL inválida. Certifique-se de incluir "http://" ou "https://".')
            return

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]

        if links:
            links_text = '\n'.join(links)
            if len(links_text) <= 2000:
                await ctx.reply(f'```🎇 Aqui estão os links encontrados em {url}:```\n```Fix\n{links_text}\n```')
            else:
                temp_file = discord.File(io.BytesIO(links_text.encode("utf-8")), filename='links.txt')
                await ctx.reply('```Fix\n🔹 Muitos links encontrados. Enviando como um arquivo:\n```', file=temp_file)
        else:
            await ctx.reply(f'Nenhum link encontrado em {url}')

        await processing_message.delete()


    @bot.tree.command(name='get_links', description='Extrai todos os links de um site. Use /get_links <url>')
    async def get_links(interaction: discord.Interaction, url: str):
        # Enviar a mensagem inicial de processamento
        processing_embed = discord.Embed(
            title='➿ Processando...',
            description=f'__🔗 Extraindo links do site__ {url}. __Por favor, aguarde.__',
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=processing_embed)

        # Verifica se a URL é válida
        if not url.startswith("http://") and not url.startswith("https://"):
            await interaction.edit_original_response(content='❌ URL inválida. Certifique-se de incluir "http://" ou "https://".')
            return

        try:
            # Faz a requisição HTTP
            response = requests.get(url)
            response.raise_for_status()

            # Faz o parsing do HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]

            # Verifica se encontrou links e edita a mensagem original com os resultados
            if links:
                links_text = '\n'.join(links)
                if len(links_text) <= 2000:
                    await interaction.edit_original_response(content=f'```🎇 Aqui estão os links encontrados em {url}:```\n```Fix\n{links_text}\n```')
                else:
                    temp_file = discord.File(io.BytesIO(links_text.encode("utf-8")), filename='links.txt')
                    await interaction.edit_original_response(content='```Fix\n🔹 Muitos links encontrados. Enviando como um arquivo:\n```', attachments=[temp_file])
            else:
                await interaction.edit_original_response(content=f'Nenhum link encontrado em {url}')
        
        # Tratamento de exceções
        except Exception as e:
            await interaction.edit_original_response(content=f'❌ Ocorreu um erro ao tentar extrair os links: {e}')