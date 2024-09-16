import discord
import requests
import random
from discord.ui import View

api_key = "AIzaSyBPGKD7aKl9rFeygkzgqrR2zEnmijK0zlY"
cse_id = "9289fa6fa16fa415e"

def setup_imagine(bot):
    class ImageView(View):
        def __init__(self, context, items):
            super().__init__()
            self.context = context
            self.items = items
            self.current_index = 0
            self.query = None

        async def show_current_image(self):
            embed = discord.Embed(
                title=f'Imagem correspondente a: {self.query}',
                color=discord.Color.green()
            )
            embed.set_image(url=self.items[self.current_index]['link'])
            if isinstance(self.context, discord.Interaction):
                embed.set_author(name=self.context.user.display_name, icon_url=self.context.user.avatar.url)
                embed.set_thumbnail(url=self.context.guild.icon.url if self.context.guild.icon else bot.user.avatar.url)
                embed.set_footer(text='Bot desenvolvido por lalaio1', icon_url=bot.user.avatar.url)
            else:
                embed.set_author(name=self.context.author.display_name, icon_url=self.context.author.avatar.url)
                embed.set_thumbnail(url=self.context.guild.icon.url if self.context.guild.icon else bot.user.avatar.url)
                embed.set_footer(text='Bot desenvolvido por lalaio1', icon_url=bot.user.avatar.url)
            embed.color = discord.Color.blue()

            if isinstance(self.context, discord.Interaction):
                self.message = await self.context.response.send_message(embed=embed)
            else:
                self.message = await self.context.reply(embed=embed)

    @bot.command(name='imagine', help='Envia uma imagem correspondente à pesquisa')
    async def search_and_send_image(ctx, *, query):
        try:
            url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}&searchType=image&num=5"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            items = data.get('items', [])

            if not items:
                await ctx.reply(f"😓 Nenhuma imagem encontrada para '{query}'.")
                return

            random.shuffle(items)

            view = ImageView(ctx, items)
            view.query = query
            await view.show_current_image()

        except requests.exceptions.RequestException as e:
            await ctx.reply(f"Erro ao buscar imagem: {str(e)}")
        except discord.HTTPException as e:
            await ctx.reply(f"Erro ao enviar embed: {str(e)}")
        except Exception as e:
            await ctx.reply(f"Ocorreu um erro inesperado: {str(e)}")

    @bot.tree.command(name='imagine', description='Envia uma imagem correspondente à pesquisa.')
    async def search_and_send_image(interaction: discord.Interaction, query: str):
        try:
            url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}&searchType=image&num=5"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            items = data.get('items', [])

            if not items:
                await interaction.response.send_message(f"😓 Nenhuma imagem encontrada para '{query}'.")
                return

            random.shuffle(items)

            view = ImageView(interaction, items)
            view.query = query
            await view.show_current_image()

        except requests.exceptions.RequestException as e:
            await interaction.response.send_message(f"Erro ao buscar imagem: {str(e)}")
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Erro ao enviar embed: {str(e)}")
        except Exception as e:
            await interaction.response.send_message(f"Ocorreu um erro inesperado: {str(e)}")
