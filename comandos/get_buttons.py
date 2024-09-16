import discord
import requests
import os
import tempfile
from bs4 import BeautifulSoup


def setup_get_buttons(bot):
    @bot.command(name='get_buttons', help='Obtém informações sobre os botões de um site. Use !get_buttons <url>')
    async def get_buttons(ctx, url):
        try:
            processing_embed = discord.Embed(
                title='Processando...',
                description=f'Obtendo informações sobre os botões do site {url}. Por favor, aguarde.',
                color=discord.Color.blue()
            )
            processing_message = await ctx.reply(embed=processing_embed)

            if not url.startswith("http://") and not url.startswith("https://"):
                await processing_message.delete()
                await ctx.reply('❌ URL inválida. Certifique-se de incluir "http://" ou "https://".')
                return

            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            buttons = soup.find_all('button')
            
            buttons_info = []

            for index, button in enumerate(buttons, start=1):
                button_text = button.get_text().strip()
                button_attrs = button.attrs
                buttons_info.append({
                    'text': button_text,
                    'attributes': button_attrs
                })

            with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.html') as temp_file:
                temp_file.write('<html><body>\n')
                temp_file.write(f'<h1>Informações sobre Botões - {url}</h1>\n')
                for index, button_info in enumerate(buttons_info, start=1):
                    temp_file.write(f'<p><b>Botão {index}:</b></p>\n')
                    temp_file.write(f'<p><b>Texto:</b> {button_info["text"]}</p>\n')
                    temp_file.write(f'<p><b>Atributos:</b> {button_info["attributes"]}</p>\n')
                    temp_file.write('<hr>\n')
                temp_file.write('</body></html>')

                temp_filename = temp_file.name

            with open(temp_filename, 'rb') as file:
                await processing_message.delete()
                await ctx.reply(file=discord.File(file, filename=f'buttons_info_{url}.html'))

                completed_embed = discord.Embed(
                    title='💫 Concluído!',
                    description=f'__Informações sobre botões do site {url} obtidas com sucesso 💠__',
                    color=discord.Color.green()
                )
                await ctx.reply(embed=completed_embed)

        except requests.exceptions.RequestException as e:
            await ctx.reply(f'Ocorreu um erro ao obter informações sobre os botões: {e}')

        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)