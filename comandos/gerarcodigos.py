
import random
import string
import tempfile
import discord
import os

def setup_gerarcodigos(bot):
    @bot.command(name='gennt')
    async def gerar_codigos(ctx, quantidade: int):
        MAX_CODIGOS = 40000
        if quantidade > MAX_CODIGOS:
            embed_limite = discord.Embed(
                title="🚫 Limite Excedido",
                description=f"O limite máximo de códigos que você pode gerar é {MAX_CODIGOS}.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed_limite)
            return

        caracteres = string.ascii_letters + string.digits
        tamanho = 24
        codigos = []

        embed_gerando = discord.Embed(
            title="🔄 Gerando Códigos",
            description="Os códigos estão sendo gerados, por favor, aguarde...",
            color=discord.Color.blue()
        )
        gerando_msg = await ctx.send(embed=embed_gerando)

        for _ in range(quantidade):
            codigo = ''.join(random.choice(caracteres) for _ in range(tamanho))
            codigos.append(f"https://discord.com/billing/promotions/{codigo}")

        codigos_str = '\n'.join(codigos)

        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
            temp_file.write(codigos_str)
            temp_file_path = temp_file.name

        embed_resultado = discord.Embed(
            title="📄 Códigos Gerados",
            description="Aqui estão os códigos gerados:",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed_resultado, file=discord.File(temp_file_path))

        await gerando_msg.delete()
        os.remove(temp_file_path)


    @bot.tree.command(name='gennt', description='Gera códigos promocionais e os envia em um arquivo.')
    async def gennt_slash(interaction: discord.Interaction, quantidade: int):
        MAX_CODIGOS = 40000
        if quantidade > MAX_CODIGOS:
            embed_limite = discord.Embed(
                title="🚫 Limite Excedido",
                description=f"O limite máximo de códigos que você pode gerar é {MAX_CODIGOS}.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed_limite)
            return

        caracteres = string.ascii_letters + string.digits
        tamanho = 24
        codigos = []

        embed_gerando = discord.Embed(
            title="🔄 Gerando Códigos",
            description="Os códigos estão sendo gerados, por favor, aguarde...",
            color=discord.Color.blue()
        )
        # Enviar mensagem inicial
        gerando_msg = await interaction.response.send_message(embed=embed_gerando)

        for _ in range(quantidade):
            codigo = ''.join(random.choice(caracteres) for _ in range(tamanho))
            codigos.append(f"https://discord.com/billing/promotions/{codigo}")

        codigos_str = '\n'.join(codigos)

        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
            temp_file.write(codigos_str)
            temp_file_path = temp_file.name

        embed_resultado = discord.Embed(
            title="📄 Códigos Gerados",
            description="Aqui estão os códigos gerados:",
            color=discord.Color.green()
        )
        # Enviar o arquivo com os códigos gerados
        await interaction.edit_original_response(content=None, embed=embed_resultado, file=discord.File(temp_file_path))

        os.remove(temp_file_path)  # Remove o arquivo temporário após o envio