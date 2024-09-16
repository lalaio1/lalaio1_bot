import discord
import requests

def setup_joke(bot):
    @bot.command(name='joke', help='Conta uma piada aleatória em português.')
    async def joke(ctx):
        try:
            # Faz a requisição à API de piadas em português
            response = requests.get('https://v2.jokeapi.dev/joke/Any?lang=pt')
            joke = response.json()

            if joke['type'] == 'single':
                joke_text = joke['joke']
                embed = discord.Embed(
                    title="🤣 Piada Aleatória",
                    description=f"{joke_text}",
                    color=discord.Color.orange()
                )
            elif joke['type'] == 'twopart':
                setup = joke['setup']
                punchline = joke['delivery']
                embed = discord.Embed(
                    title="🤣 Piada Aleatória",
                    description=f"{setup}\n\n{punchline}",
                    color=discord.Color.orange()
                )
            
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Buscar Piada",
                description=f"Ocorreu um erro ao tentar buscar uma piada: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)


    @bot.tree.command(name='joke', description='Conta uma piada aleatória em português.')
    async def joke(interaction: discord.Interaction):
        try:
            # Faz a requisição à API de piadas em português
            response = requests.get('https://v2.jokeapi.dev/joke/Any?lang=pt')
            joke = response.json()

            if joke['type'] == 'single':
                joke_text = joke['joke']
                embed = discord.Embed(
                    title="🤣 Piada Aleatória",
                    description=f"{joke_text}",
                    color=discord.Color.orange()
                )
            elif joke['type'] == 'twopart':
                setup = joke['setup']
                punchline = joke['delivery']
                embed = discord.Embed(
                    title="🤣 Piada Aleatória",
                    description=f"{setup}\n\n{punchline}",
                    color=discord.Color.orange()
                )
            
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Buscar Piada",
                description=f"Ocorreu um erro ao tentar buscar uma piada: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed)
