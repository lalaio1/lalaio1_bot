import random
import discord
import string

def setup_password(bot):
    @bot.command(name='password', help='Gera uma senha segura com o comprimento especificado. Uso: A.password <comprimento>')
    async def generate_password(ctx, length: int):
        try:
            if length < 4:
                embed = discord.Embed(
                    title="Erro ao Gerar Senha",
                    description="O comprimento da senha deve ser pelo menos 4.",
                    color=discord.Color.red()
                )
                await ctx.reply(embed=embed)
                return
            elif length > 64:
                embed = discord.Embed(
                    title="Erro ao Gerar Senha",
                    description="O comprimento máximo da senha permitido é 64.",
                    color=discord.Color.red()
                )
                await ctx.reply(embed=embed)
                return

            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(characters) for _ in range(length))
            
            formatted_password = f"```{password}```"

            embed = discord.Embed(
                title="🔒 Senha Segura Gerada",
                description=f"**Senha:** {formatted_password}",
                color=discord.Color.green()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await ctx.reply(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="Erro ao Gerar Senha",
                description="Por favor, forneça um número inteiro válido para o comprimento da senha.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Erro ao Gerar Senha",
                description=f"Ocorreu um erro ao gerar a senha: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)

    @bot.tree.command(name='password', description='Gera uma senha segura com o comprimento especificado. Uso: /password <comprimento>')
    async def generate_password(interaction: discord.Interaction, length: int):
        try:
            if length < 4:
                embed = discord.Embed(
                    title="Erro ao Gerar Senha",
                    description="O comprimento da senha deve ser pelo menos 4.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            elif length > 64:
                embed = discord.Embed(
                    title="Erro ao Gerar Senha",
                    description="O comprimento máximo da senha permitido é 64.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(characters) for _ in range(length))
            
            formatted_password = f"```{password}```"

            embed = discord.Embed(
                title="🔒 Senha Segura Gerada",
                description=f"**Senha:** {formatted_password}",
                color=discord.Color.green()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await interaction.response.send_message(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="Erro ao Gerar Senha",
                description="Por favor, forneça um número inteiro válido para o comprimento da senha.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            embed = discord.Embed(
                title="Erro ao Gerar Senha",
                description=f"Ocorreu um erro ao gerar a senha: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)