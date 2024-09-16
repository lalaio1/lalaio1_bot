import discord
import random

def setup_shuffle(bot):
    @bot.command(name='shuffle', help='Embaralha as palavras de uma frase. Uso: A.shuffle <frase>')
    async def shuffle(ctx, *, sentence: str):
        words = sentence.split()
        
        if len(words) <= 1:
            embed = discord.Embed(
                title="⚠️ Embaralhamento Não Possível!",
                description="Por favor, forneça uma frase com mais de uma palavra para embaralhar.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://emojicombos.com/files/emoji-one/letter-x-emoji-one.png")
            await ctx.reply(embed=embed)
            return
        
        random.shuffle(words)
        shuffled_sentence = ' '.join(words)
        
        embed = discord.Embed(
            title="🔀 Palavras Embaralhadas",
            description=f"**Frase Original:**\n`{sentence}`\n\n**Frase Embaralhada:**\n`{shuffled_sentence}`",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        
        await ctx.reply(embed=embed)

    @bot.tree.command(name='shuffle', description='Embaralha as palavras de uma frase.')
    async def shuffle(interaction: discord.Interaction, sentence: str):
        words = sentence.split()
        
        if len(words) <= 1:
            embed = discord.Embed(
                title="⚠️ Embaralhamento Não Possível!",
                description="Por favor, forneça uma frase com mais de uma palavra para embaralhar.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="https://emojicombos.com/files/emoji-one/letter-x-emoji-one.png")
            await interaction.response.send_message(embed=embed)
            return
        
        random.shuffle(words)
        shuffled_sentence = ' '.join(words)
        
        embed = discord.Embed(
            title="🔀 Palavras Embaralhadas",
            description=f"**Frase Original:**\n`{sentence}`\n\n**Frase Embaralhada:**\n`{shuffled_sentence}`",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        
        await interaction.response.send_message(embed=embed)