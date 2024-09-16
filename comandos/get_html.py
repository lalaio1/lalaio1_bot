import discord 
import requests
import tempfile
import os 


def setup_get_html(bot):
    @bot.command(name='get_html', help='Obtém o código HTML de um site. Use !get_html <url>')
    async def get_html(ctx, url):
        try:
            processing_embed = discord.Embed(
                title='➿ Processando...',
                description=f'🍃 __Obtendo o código HTML do site__ {url}',
                color=discord.Color.blue()
            )
            processing_message = await ctx.reply(embed=processing_embed)

            response = requests.get(url)
            response.raise_for_status()  

            with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.html') as temp_file:
                temp_file.write(response.text)
                temp_filename = temp_file.name

            if len(response.text) <= 2000:
                await processing_message.delete()  
                await ctx.reply(f'```html\n{response.text}\n```')
            else:
                with open(temp_filename, 'rb') as file:
                    await processing_message.delete()  
                    await ctx.reply(file=discord.File(file, filename=f'html_{url}.html'))

            completed_embed = discord.Embed(
                title='💫 Concluído!',
                description=f'__Código HTML do site__ {url} __obtido com sucesso__ 💠',
                color=discord.Color.green()
            )
            await ctx.reply(embed=completed_embed)

        except requests.exceptions.RequestException as e:
            await ctx.reply(f'```Diff\n-Ocorreu um erro ao obter o código HTML:```\n `{e}`')

        finally:
            os.remove(temp_filename)


