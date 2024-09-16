import discord
from discord.ext import commands
import random
import json

def load_secrets(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['secrets']

# Defina o caminho do arquivo JSON diretamente
json_path = r'/home/lalaio1/lalaio1 bot/json/pysch/psychologist.json'  # Substitua pelo caminho desejado
secrets = load_secrets(json_path)

def setup_psicologo(bot):
    @bot.command(name='psicologo')
    async def psicologo(ctx, member: discord.Member):
        secret = random.choice(secrets)

        embed = discord.Embed(
            title="🔮 Análise Psicológica 🔮",
            description=f"**{member.mention}** {secret}",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Essa analise é completamente real")

        await ctx.send(embed=embed)

    @bot.tree.command(name='psicologo', description='Fornece uma análise psicológica divertida sobre o membro mencionado.')
    async def psicologo(interaction: discord.Interaction, member: discord.Member):
        secret = random.choice(secrets)

        embed = discord.Embed(
            title="🔮 Análise Psicológica 🔮",
            description=f"**{member.mention}** {secret}",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Essa análise é completamente real")

        # Envia a resposta e exclui a mensagem original
        await interaction.response.send_message(embed=embed)