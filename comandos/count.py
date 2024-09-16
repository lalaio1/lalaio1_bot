import discord
from discord.ext import commands

def setup_count(bot):
    @bot.command(name='count', help='Conta o número de caracteres, palavras e linhas em um texto. Uso: A.count <texto>')
    async def count_text(ctx, *, text: str):
        try:
            num_characters = len(text)
            num_words = len(text.split())
            num_lines = text.count('\n') + 1  
            
            embed = discord.Embed(
                title="🔢 Contagem de Texto",
                description=f"**Caracteres:** {num_characters}\n**Palavras:** {num_words}\n**Linhas:** {num_lines}",
                color=discord.Color.green()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await ctx.reply(embed=embed)
        
        except Exception as e:
            embed = discord.Embed(
                title="🚫 Erro ao Contar Texto",
                description=f"Ocorreu um erro ao contar o texto:\n```{str(e)}```",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)


    @bot.tree.command(name='count', description='Conta o número de caracteres, palavras e linhas em um texto.')
    @discord.app_commands.describe(text='O texto a ser contado')
    async def count_text(interaction: discord.Interaction, text: str):
        try:
            num_characters = len(text)
            num_words = len(text.split())
            num_lines = text.count('\n') + 1  
            
            embed = discord.Embed(
                title="🔢 Contagem de Texto",
                description=f"**Caracteres:** {num_characters}\n**Palavras:** {num_words}\n**Linhas:** {num_lines}",
                color=discord.Color.green()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            embed = discord.Embed(
                title="🚫 Erro ao Contar Texto",
                description=f"Ocorreu um erro ao contar o texto:\n```{str(e)}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)

    @count_text.error
    async def count_text_error(interaction: discord.Interaction, error):
        embed = discord.Embed(
            title="🚫 Erro",
            description="Ocorreu um erro ao processar sua solicitação. Verifique o texto e tente novamente.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)