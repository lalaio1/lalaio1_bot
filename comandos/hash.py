import hashlib
import discord
from discord.ext import commands



def generate_hash(message: str, hash_type: str) -> str:
    """Gera um hash da mensagem com base no tipo de hash especificado."""
    if hash_type == 'md5':
        hash_object = hashlib.md5(message.encode())
    elif hash_type == 'sha1':
        hash_object = hashlib.sha1(message.encode())
    elif hash_type == 'sha256':
        hash_object = hashlib.sha256(message.encode())
    elif hash_type == 'sha512':
        hash_object = hashlib.sha512(message.encode())
    else:
        raise ValueError("Tipo de hash não suportado.")
    
    return hash_object.hexdigest()

def setup_hash(bot):
    @bot.command(name='hash', help='Gera um hash de uma mensagem. Uso: A.hash <tipo> <mensagem>. Tipos: md5, sha1, sha256, sha512')
    async def hash_message(ctx, hash_type: str, *, message: str):
        if not message:
            await ctx.reply("Por favor, forneça uma mensagem para gerar o hash.")
            return
        
        valid_hash_types = ['md5', 'sha1', 'sha256', 'sha512']
        
        if hash_type.lower() not in valid_hash_types:
            await ctx.reply(f"Tipo de hash inválido. Tipos suportados: {', '.join(valid_hash_types)}")
            return

        try:
            hash_result = generate_hash(message, hash_type.lower())
            
            embed = discord.Embed(
                title=f"🔑 Hash {hash_type.upper()}",
                description=f"```{hash_result}```",
                color=discord.Color.blue()
            )
            embed.add_field(name="Mensagem Original:", value=f"`{message}`", inline=False)
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await ctx.reply(embed=embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Gerar Hash",
                description=f"Ocorreu um erro ao tentar gerar o hash: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)

    @bot.tree.command(name='hash', description='Gera um hash de uma mensagem. Tipos: md5, sha1, sha256, sha512.')
    async def hash_message(interaction: discord.Interaction, hash_type: str, message: str):
        valid_hash_types = ['md5', 'sha1', 'sha256', 'sha512']
        
        if hash_type.lower() not in valid_hash_types:
            await interaction.response.send_message(
                f"Tipo de hash inválido. Tipos suportados: {', '.join(valid_hash_types)}",
                ephemeral=True
            )
            return

        if not message:
            await interaction.response.send_message("Por favor, forneça uma mensagem para gerar o hash.", ephemeral=True)
            return

        try:
            hash_result = generate_hash(message, hash_type.lower())
            
            embed = discord.Embed(
                title=f"🔑 Hash {hash_type.upper()}",
                description=f"```{hash_result}```",
                color=discord.Color.blue()
            )
            embed.add_field(name="Mensagem Original:", value=f"`{message}`", inline=False)
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Gerar Hash",
                description=f"Ocorreu um erro ao tentar gerar o hash: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed)