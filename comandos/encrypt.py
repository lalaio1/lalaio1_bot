import os
import discord
import base64
from discord import Embed
from discord.ext import commands
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets

secret_key = secrets.token_bytes(32)

async def encrypt_message(ctx_or_interaction, *, message):
    try:
        message_bytes = message.encode('utf-8')
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(secret_key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message_bytes) + encryptor.finalize()
        tag = encryptor.tag
        encrypted_message = base64.urlsafe_b64encode(iv + ciphertext + tag).decode('utf-8')

        embed = Embed(
            title="Mensagem Criptografada",
            description="Aqui está a mensagem criptografada:",
            color=0x00ff00
        )
        embed.set_thumbnail(url="https://i.ibb.co/kGrGJk4/40-104848.png")
        embed.add_field(name="Mensagem Original", value=f"```{message}```", inline=False)
        embed.add_field(name="IV (Inicialização)", value=f"```{base64.urlsafe_b64encode(iv).decode('utf-8')}```", inline=False)
        embed.add_field(name="Texto Criptografado", value=f"```Fix\n{encrypted_message}\n```", inline=False)
        embed.set_footer(text="Criptografia AES-GCM", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")

        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.reply(embed=embed)

    except Exception as e:
        error_embed = discord.Embed(description=f"Ocorreu um erro durante a criptografia: {str(e)}", color=discord.Color.red())
        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=error_embed)
        else:
            await ctx_or_interaction.reply(embed=error_embed)

async def decrypt_message(ctx_or_interaction, *, encrypted_message):
    try:
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_message.encode('utf-8'))

        iv = encrypted_bytes[:16]
        ciphertext_with_tag = encrypted_bytes[16:]

        cipher = Cipher(algorithms.AES(secret_key), modes.GCM(iv, ciphertext_with_tag[-16:]), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_message_bytes = decryptor.update(ciphertext_with_tag[:-16]) + decryptor.finalize()
        decrypted_message = decrypted_message_bytes.decode('utf-8')

        embed = Embed(
            title="Mensagem Descriptografada",
            description="Aqui está a mensagem descriptografada:",
            color=0x0000ff
        )
        embed.set_thumbnail(url="https://i.ibb.co/kGrGJk4/40-104848.png")
        embed.add_field(name="Texto Criptografado Recebido", value=f"```{encrypted_message}```", inline=False)
        embed.add_field(name="IV Usado", value=f"```{base64.urlsafe_b64encode(iv).decode('utf-8')}```", inline=False)
        embed.add_field(name="Mensagem Descriptografada", value=f"```Fix\n{decrypted_message}\n```", inline=False)
        embed.set_footer(text="Descriptografia AES-GCM", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")

        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.reply(embed=embed)

    except Exception as e:
        error_embed = discord.Embed(description=f"Ocorreu um erro durante a descriptografia: {str(e)}", color=discord.Color.red())
        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=error_embed)
        else:
            await ctx_or_interaction.reply(embed=error_embed)

def setup_encrypt(bot):
    @bot.command(name='encrypt', help='Criptografa uma mensagem usando AES-GCM')
    async def encrypt_command(ctx, *, message):
        await encrypt_message(ctx, message=message)

    @bot.command(name='decrypt', help='Descriptografa uma mensagem previamente criptografada com AES-GCM')
    async def decrypt_command(ctx, *, encrypted_message):
        await decrypt_message(ctx, encrypted_message=encrypted_message)

    @bot.tree.command(name='encrypt', description='Criptografa uma mensagem usando AES-GCM')
    async def encrypt_slash(interaction: discord.Interaction, message: str):
        await encrypt_message(interaction, message=message)

    @bot.tree.command(name='decrypt', description='Descriptografa uma mensagem previamente criptografada com AES-GCM')
    async def decrypt_slash(interaction: discord.Interaction, encrypted_message: str):
        await decrypt_message(interaction, encrypted_message=encrypted_message)
