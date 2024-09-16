import discord
from discord.ext import commands
from validate_docbr import CPF
import tempfile
import os
import itertools

def setup_cpf(bot):
    @bot.command(name='checkcpf', help='Valida um CPF.')
    async def check_cpf(ctx, cpf_number: str):
        cpf = CPF()
        if cpf.validate(cpf_number):
            result = f"O CPF {cpf_number} é válido."
            color = discord.Color.green()
        else:
            result = f"O CPF {cpf_number} é inválido."
            color = discord.Color.red()
        
        embed = discord.Embed(
            title="Validação de CPF",
            description=result,
            color=color
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        embed.set_thumbnail(url="https://i.ibb.co/zN5t8mv/cpf-icone.png")
        
        await ctx.reply(embed=embed)

    @bot.command(name='generatecpf', help='Gera CPFs válidos. Uso: L.generatecpf <quantidade>')
    async def generate_cpf(ctx, quantidade: int):
        if quantidade < 1 or quantidade > 500:
            await ctx.reply("```Por favor, forneça uma quantidade entre 1 e 500.```")
            return
        
        loading_message = await ctx.reply("```Gerando CPFs... ⏳```")

        cpf = CPF()
        cpfs_gerados = [cpf.generate() for _ in range(quantidade)]
        result = "\n".join(cpfs_gerados)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp:
            temp.write(result.encode())
            temp_path = temp.name
        
        await loading_message.delete()
        
        embed = discord.Embed(
            title="Gerador de CPFs",
            description=f"**Quantidade de CPFs gerados:** {quantidade}",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        embed.set_thumbnail(url="https://i.ibb.co/zN5t8mv/cpf-icone.png")
        
        await ctx.reply(embed=embed, file=discord.File(temp_path))
        
        # Remove o arquivo temporário após o envio
        os.remove(temp_path)

    @bot.command(name='findcpf', help='Encontra CPFs válidos a partir de um padrão. Uso: L.findcpf <padrão>')
    async def find_cpf(ctx, pattern: str):
        if len(pattern) != 11:
            await ctx.reply("```O padrão deve ter 11 caracteres.```")
            return
        
        loading_message = await ctx.reply("```Procurando CPFs válidos... ⏳```")
        
        cpf = CPF()
        cpfs_validos = []
        for comb in itertools.product('0123456789', repeat=pattern.count('*')):
            cpf_tentativa = list(pattern)
            comb_idx = 0
            for i in range(len(cpf_tentativa)):
                if cpf_tentativa[i] == '*':
                    cpf_tentativa[i] = comb[comb_idx]
                    comb_idx += 1
            cpf_tentativa = ''.join(cpf_tentativa)
            if cpf.validate(cpf_tentativa):
                cpfs_validos.append(cpf_tentativa)
        
        result = "\n".join(cpfs_validos)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp:
            temp.write(result.encode())
            temp_path = temp.name
        
        await loading_message.delete()
        
        embed = discord.Embed(
            title="Busca de CPFs",
            description=f"**CPFs válidos encontrados:** {len(cpfs_validos)}",
            color=discord.Color.green()
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        embed.set_thumbnail(url="https://i.ibb.co/zN5t8mv/cpf-icone.png")
        
        await ctx.reply(embed=embed, file=discord.File(temp_path))
        
        os.remove(temp_path)

    @bot.tree.command(name='checkcpf', description='Valida um CPF.')
    @discord.app_commands.describe(cpf_number='O CPF a ser validado')
    async def check_cpf(interaction: discord.Interaction, cpf_number: str):
        cpf = CPF()
        if cpf.validate(cpf_number):
            result = f"O CPF {cpf_number} é válido."
            color = discord.Color.green()
        else:
            result = f"O CPF {cpf_number} é inválido."
            color = discord.Color.red()
        
        embed = discord.Embed(
            title="Validação de CPF",
            description=result,
            color=color
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        embed.set_thumbnail(url="https://i.ibb.co/zN5t8mv/cpf-icone.png")
        
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='generatecpf', description='Gera CPFs válidos.')
    @discord.app_commands.describe(quantidade='Número de CPFs a serem gerados')
    async def generate_cpf(interaction: discord.Interaction, quantidade: int):
        if quantidade < 1 or quantidade > 500:
            await interaction.response.send_message("```Por favor, forneça uma quantidade entre 1 e 500.```", ephemeral=True)
            return
        
        # Envie uma mensagem de carregamento e capture o ID da mensagem
        loading_message = await interaction.response.send_message("```Gerando CPFs... ⏳```")

        cpf = CPF()
        cpfs_gerados = [cpf.generate() for _ in range(quantidade)]
        result = "\n".join(cpfs_gerados)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp:
            temp.write(result.encode())
            temp_path = temp.name
        
        # Atualize a mensagem de carregamento com a mensagem final e envie o arquivo
        await interaction.response.edit_message(content="```Gerador de CPFs concluído!```", file=discord.File(temp_path))
        
        # Remove o arquivo temporário após o envio
        os.remove(temp_path)

    @bot.tree.command(name='findcpf', description='Encontra CPFs válidos a partir de um padrão.')
    @discord.app_commands.describe(pattern='Padrão para encontrar CPFs (deve ter 11 caracteres, com * para substituição)')
    async def find_cpf(interaction: discord.Interaction, pattern: str):
        if len(pattern) != 11:
            await interaction.response.send_message("```O padrão deve ter 11 caracteres.```", ephemeral=True)
            return
        
        loading_message = await interaction.response.send_message("```Procurando CPFs válidos... ⏳```")
        
        cpf = CPF()
        cpfs_validos = []
        for comb in itertools.product('0123456789', repeat=pattern.count('*')):
            cpf_tentativa = list(pattern)
            comb_idx = 0
            for i in range(len(cpf_tentativa)):
                if cpf_tentativa[i] == '*':
                    cpf_tentativa[i] = comb[comb_idx]
                    comb_idx += 1
            cpf_tentativa = ''.join(cpf_tentativa)
            if cpf.validate(cpf_tentativa):
                cpfs_validos.append(cpf_tentativa)
        
        result = "\n".join(cpfs_validos)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp:
            temp.write(result.encode())
            temp_path = temp.name
        
        await loading_message.delete()
        
        embed = discord.Embed(
            title="Busca de CPFs",
            description=f"**CPFs válidos encontrados:** {len(cpfs_validos)}",
            color=discord.Color.green()
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        embed.set_thumbnail(url="https://i.ibb.co/zN5t8mv/cpf-icone.png")
        
        await interaction.response.send_message(embed=embed, file=discord.File(temp_path))
        
        os.remove(temp_path)