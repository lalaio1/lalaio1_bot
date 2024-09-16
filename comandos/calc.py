import discord
import math
import re


def safe_eval(expr):
    allowed_chars = re.compile(r'^[0-9+\-*/()., sqrt pow sin cos tan pi e]+$')
    if not allowed_chars.match(expr.replace(' ', '')):
        raise ValueError("Expressão inválida")

    expr = expr.replace('sqrt', 'math.sqrt')
    expr = expr.replace('pow', 'math.pow')
    expr = expr.replace('sin', 'math.sin')
    expr = expr.replace('cos', 'math.cos')
    expr = expr.replace('tan', 'math.tan')
    expr = expr.replace('pi', 'math.pi')
    expr = expr.replace('e', 'math.e')
    
    try:
        return eval(expr, {"math": math})
    except Exception as e:
        raise ValueError("Erro na avaliação da expressão") from e

def setup_calc(bot):
    @bot.command(name='calc', help='Calcula uma expressão matemática. Uso: A.calc <expressão>')
    async def calc(ctx, *, expression: str):
        try:
            result = safe_eval(expression)
            embed = discord.Embed(
                title="📊 Resultado do Cálculo",
                description=f"**Expressão:** `{expression}`\n**Resultado:** `{result}`",
                color=discord.Color.green()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)
        except ValueError as e:
            embed = discord.Embed(
                title="🚫 Erro no Cálculo",
                description=f"**Expressão:** `{expression}`\n**Erro:** `{str(e)}`",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)

    @bot.tree.command(name='calc', description='Calcula uma expressão matemática. Uso: A.calc <expressão>')
    async def calc(interaction: discord.Interaction, *, expression: str):
        try:
            result = safe_eval(expression)
            embed = discord.Embed(
                title="📊 Resultado do Cálculo",
                description=f"**Expressão:** `{expression}`\n**Resultado:** `{result}`",
                color=discord.Color.green()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)
        except ValueError as e:
            embed = discord.Embed(
                title="🚫 Erro no Cálculo",
                description=f"**Expressão:** `{expression}`\n**Erro:** `{str(e)}`",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)