import discord

def setup_to_binary(bot):
    @bot.command(name='to_binary', help='Converte uma mensagem para binário. Uso: A.to_binary <mensagem>')
    async def to_binary(ctx, *, message: str):
        binary_message = ' '.join(format(ord(char), '08b') for char in message)
        
        embed = discord.Embed(
            title="🔠 Mensagem Convertida para Binário",
            description=f"**Mensagem Original:** `{message}`\n\n```{binary_message}```",
            color=discord.Color.gold()
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        
        await ctx.reply(embed=embed)

    @bot.tree.command(name='to_binary', description='Converte uma mensagem para binário. Uso: A.to_binary <mensagem>')
    async def to_binary(interaction: discord.Interaction, message: str):
        binary_message = ' '.join(format(ord(char), '08b') for char in message)
        
        embed = discord.Embed(
            title="🔠 Mensagem Convertida para Binário",
            description=f"**Mensagem Original:** `{message}`\n\n```{binary_message}```",
            color=discord.Color.gold()
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        
        await interaction.response.send_message(embed=embed)

    