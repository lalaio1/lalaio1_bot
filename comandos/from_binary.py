import discord

def setup_from_binary(bot):
    @bot.command(name='from_binary', help='Lê uma mensagem binária e converte para texto. Uso: A.from_binary <binário>')
    async def from_binary(ctx, *, binary: str):
        if not binary:
            embed = discord.Embed(
                title="Erro",
                description="Por favor, forneça uma sequência binária para decodificar.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return
        
        # Verifica se a sequência binária contém apenas '0' e '1'
        if not all(char in '01' for char in binary):
            embed = discord.Embed(
                title="Erro",
                description="A sequência binária deve conter apenas '0' e '1'.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        # Remove espaços em branco da sequência binária
        binary = binary.replace(" ", "")

        # Converte a sequência binária para texto
        try:
            message = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
            
            embed = discord.Embed(
                title="🔠 Mensagem Binária Decodificada",
                description=f"```{message}```",
                color=discord.Color.teal()
            )
            embed.add_field(name="Binário:", value=f"```{binary}```", inline=False)
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await ctx.reply(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="Erro",
                description="A sequência binária não está em um formato válido para decodificação.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        
        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Decodificar Binário",
                description=f"Ocorreu um erro ao tentar decodificar a sequência binária: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)

    @bot.tree.command(name='from_binary', description='Lê uma mensagem binária e converte para texto.')
    async def from_binary_slash(interaction: discord.Interaction, binary: str):
        if not binary:
            embed = discord.Embed(
                title="Erro",
                description="Por favor, forneça uma sequência binária para decodificar.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Verifica se a sequência binária contém apenas '0' e '1'
        if not all(char in '01' for char in binary):
            embed = discord.Embed(
                title="Erro",
                description="A sequência binária deve conter apenas '0' e '1'.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        # Remove espaços em branco da sequência binária
        binary = binary.replace(" ", "")

        # Converte a sequência binária para texto
        try:
            message = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
            
            embed = discord.Embed(
                title="🔠 Mensagem Binária Decodificada",
                description=f"```{message}```",
                color=discord.Color.teal()
            )
            embed.add_field(name="Binário:", value=f"```{binary}```", inline=False)
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await interaction.response.send_message(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="Erro",
                description="A sequência binária não está em um formato válido para decodificação.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Decodificar Binário",
                description=f"Ocorreu um erro ao tentar decodificar a sequência binária: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed)