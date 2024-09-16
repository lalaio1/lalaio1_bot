import discord
from discord.ext import commands

def setup_colorinfo(bot):
    @bot.command(name='colorinfo', aliases=['rgb', 'hexcolor', 'hex', 'colorpick', 'colorpicker'])
    async def color_info(ctx, *, color: str):
        try:
            if color.startswith('#'):
                hex_color = color.lstrip('#')
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            elif ',' in color:
                rgb_color = tuple(map(int, color.split(',')))
                hex_color = '{:02x}{:02x}{:02x}'.format(*rgb_color)
            elif color.startswith('-'):
                decimal_color = int(color)
                hex_color = '{:06x}'.format(decimal_color & 0xFFFFFF)
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                raise ValueError("Invalid color format")

            discord_color = discord.Color.from_rgb(*rgb_color)

            embed = discord.Embed(
                title="🎨 Informações da Cor",
                color=discord_color
            )
            embed.add_field(name="RGB", value=f"```{rgb_color}```", inline=True)
            embed.add_field(name="Hexadecimal", value=f"```#{hex_color}```", inline=True)
            embed.add_field(name="Decimal", value=f"```{int(hex_color, 16)}```", inline=True)
            embed.set_thumbnail(url=f"https://singlecolorimage.com/get/{hex_color}/100x100")

            embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="🚫 Erro",
                description="Formato de cor inválido. Use um dos formatos válidos: `RGB`, `#Hex`, ou `Decimal`.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)

    @color_info.error
    async def color_info_error(ctx, error):
        embed = discord.Embed(
            title="🚫 Erro",
            description="Ocorreu um erro ao processar sua solicitação. Verifique o formato da cor e tente novamente.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @bot.tree.command(name='colorinfo', description='Obtém informações sobre uma cor em RGB, Hex ou Decimal.')
    @discord.app_commands.describe(color='A cor a ser analisada (RGB, #Hex, ou Decimal)')
    async def color_info(interaction: discord.Interaction, color: str):
        try:
            if color.startswith('#'):
                hex_color = color.lstrip('#')
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            elif ',' in color:
                rgb_color = tuple(map(int, color.split(',')))
                hex_color = '{:02x}{:02x}{:02x}'.format(*rgb_color)
            elif color.startswith('-'):
                decimal_color = int(color)
                hex_color = '{:06x}'.format(decimal_color & 0xFFFFFF)
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                raise ValueError("Invalid color format")

            discord_color = discord.Color.from_rgb(*rgb_color)

            embed = discord.Embed(
                title="🎨 Informações da Cor",
                color=discord_color
            )
            embed.add_field(name="RGB", value=f"```{rgb_color}```", inline=True)
            embed.add_field(name="Hexadecimal", value=f"```#{hex_color}```", inline=True)
            embed.add_field(name="Decimal", value=f"```{int(hex_color, 16)}```", inline=True)
            embed.set_thumbnail(url=f"https://singlecolorimage.com/get/{hex_color}/100x100")

            embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="🚫 Erro",
                description="Formato de cor inválido. Use um dos formatos válidos: `RGB`, `#Hex`, ou `Decimal`.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @color_info.error
    async def color_info_error(interaction: discord.Interaction, error):
        embed = discord.Embed(
            title="🚫 Erro",
            description="Ocorreu um erro ao processar sua solicitação. Verifique o formato da cor e tente novamente.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)