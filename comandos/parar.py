import discord
from discord.ext import commands
import subprocess
from discord import app_commands


async def is_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.administrator

def setup_desligar(bot):
    @bot.tree.command(name='desligar', description='Desliga o bot e atualiza o status do canal de voz')
    @app_commands.check(is_admin)
    async def desligar(interaction: discord.Interaction):
        # Verifica se o usuário é o dono ou está na equipe
        if interaction.user.id != bot.owner_id and interaction.user.id not in [1169336831310041209, 1169781984927686696, 1239967192154378280, 1240390499441840140]:
            embed = discord.Embed(
                title='❌ Acesso Negado',
                description="Você não tem permissão para usar este comando.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)
            return

        # Atualiza o status do canal de voz
        channel = bot.get_channel(1267582290301550644)  # Substitua pelo ID do seu canal de voz
        if channel:
            await channel.edit(name="STATUS L1 BOT 🔴")
        
        # Envia uma mensagem bonita de desligamento
        embed = discord.Embed(
            title='🔒 Desligando...',
            description="O bot está sendo desligado agora. Até a próxima!",
            color=discord.Color.orange()
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        await interaction.response.send_message(embed=embed)

        # Muda o status do bot para offline
        await bot.change_presence(status=discord.Status.invisible)

        # Desliga o bot
        await bot.close()

    @bot.tree.command(name='reiniciar', description='Reinicia o bot')
    @app_commands.check(is_admin)
    async def reiniciar(interaction: discord.Interaction):
        # Verifica se o usuário é o dono ou está na equipe
        if interaction.user.id != bot.owner_id and interaction.user.id not in [1169336831310041209, 1169781984927686696]:
            embed = discord.Embed(
                title='❌ Acesso Negado',
                description="Você não tem permissão para usar este comando.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)
            return

        # Envia uma mensagem bonita de reinício
        embed = discord.Embed(
            title='🔄 Reiniciando...',
            description="O bot está sendo reiniciado agora. Por favor, aguarde!",
            color=discord.Color.orange()
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        await interaction.response.send_message(embed=embed)

        script_path = r'/home/lalaio1/lalaio1 bot/scripts/reiniciar/restart.py'
        try:
            subprocess.Popen(['python', f'{script_path}'])
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro ao Reiniciar',
                description=f"Ocorreu um erro ao tentar reiniciar o bot: {e}",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)

        # Desliga o bot
        await bot.close()