import discord
import requests
from discord.ext import commands

def setup_define(bot):
    @bot.command(name='define', help='Fornece a definição de uma palavra. Uso: A.define <palavra>')
    async def define(ctx, *, word: str):
        try:
            response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
            definitions = response.json()

            if 'title' in definitions and definitions['title'] == "No Definitions Found":
                embed = discord.Embed(
                    title="📚 Definição",
                    description=f"Não foi possível encontrar a definição para a palavra `{word}`.",
                    color=discord.Color.red()
                )
            else:
                definition = definitions[0]['meanings'][0]['definitions'][0]['definition']
                embed = discord.Embed(
                    title="📚 Definição",
                    description=f"**Palavra:** `{word}`\n**Definição:** {definition}",
                    color=discord.Color.blue()
                )

            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)

        except requests.exceptions.RequestException as e:
            embed = discord.Embed(
                title="Erro de Requisição",
                description=f"😫 Ocorreu um erro ao acessar a definição da palavra `{word}`: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Erro Inesperado",
                description=f"😟 Ocorreu um erro inesperado ao processar a definição da palavra `{word}`: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)


    @bot.tree.command(name='define', description='Fornece a definição de uma palavra.')
    @discord.app_commands.describe(word='A palavra para obter a definição')
    async def define(interaction: discord.Interaction, word: str):
        try:
            response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
            definitions = response.json()

            if 'title' in definitions and definitions['title'] == "No Definitions Found":
                embed = discord.Embed(
                    title="📚 Definição",
                    description=f"Não foi possível encontrar a definição para a palavra `{word}`.",
                    color=discord.Color.red()
                )
            else:
                definition = definitions[0]['meanings'][0]['definitions'][0]['definition']
                embed = discord.Embed(
                    title="📚 Definição",
                    description=f"**Palavra:** `{word}`\n**Definição:** {definition}",
                    color=discord.Color.blue()
                )

            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)

        except requests.exceptions.RequestException as e:
            embed = discord.Embed(
                title="Erro de Requisição",
                description=f"😫 Ocorreu um erro ao acessar a definição da palavra `{word}`: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Erro Inesperado",
                description=f"😟 Ocorreu um erro inesperado ao processar a definição da palavra `{word}`: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)