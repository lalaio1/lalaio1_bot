import discord
from discord.ext import commands
import aiohttp
from PIL import Image
from io import BytesIO
import asyncio


async def get_image_color(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image_bytes = await response.read()
            image = Image.open(BytesIO(image_bytes))
            image = image.convert('RGB')
            pixels = list(image.getdata())
            avg_color = tuple(sum(col) // len(col) for col in zip(*pixels))
            return discord.Color.from_rgb(*avg_color), image_bytes
            
def setup_addemoji(bot):
    @bot.command(name='addemoji')
    @commands.has_permissions(manage_emojis=True)
    async def add_emoji(ctx, emoji: str):
        try:
            emoji_id = None
            emoji_name = None

            if emoji.startswith('<:') and emoji.endswith('>'):
                emoji_id = emoji.split(':')[2][:-1]
            elif emoji.startswith('<a:') and emoji.endswith('>'):
                emoji_id = emoji.split(':')[2][:-1]
            elif emoji.startswith(':') and emoji.endswith(':'):
                emoji_name = emoji.strip(':')
            else:
                embed = discord.Embed(
                    title="🚫 Erro",
                    description="Por favor, forneça um nome de emoji válido no formato `:nome_do_emoji:` ou um emoji com ID no formato `<:emoji_nome:emoji_id>`.",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
                await ctx.reply(embed=embed)
                return

            emoji_to_add = None

            if emoji_id:
                for guild in bot.guilds:
                    emoji_to_add = discord.utils.get(guild.emojis, id=int(emoji_id))
                    if emoji_to_add:
                        break
            elif emoji_name:
                for guild in bot.guilds:
                    emoji_to_add = discord.utils.get(guild.emojis, name=emoji_name)
                    if emoji_to_add:
                        break

            if not emoji_to_add:
                embed = discord.Embed(
                    title="🚫 Emoji Não Encontrado",
                    description=f"O emoji `{emoji}` não foi encontrado em nenhum servidor onde o bot está presente.",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
                await ctx.reply(embed=embed)
                return

            emoji_url = str(emoji_to_add.url)
            avg_color, image_bytes = await get_image_color(emoji_url)

            guild = ctx.guild

            if len(guild.emojis) >= guild.emoji_limit:
                embed = discord.Embed(
                    title="⚠️ Limite de Emojis Atingido",
                    description="O servidor já atingiu o limite máximo de emojis.",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
                await ctx.reply(embed=embed)
                return

            existing_emoji = discord.utils.get(guild.emojis, name=emoji_to_add.name)
            if existing_emoji:
                await existing_emoji.delete()

            new_emoji = await guild.create_custom_emoji(name=emoji_to_add.name, image=image_bytes)

            embed = discord.Embed(
                title="✅ Emoji Adicionado com Sucesso!",
                description=f"O emoji `{new_emoji.name}` foi adicionado ao servidor com sucesso!",
                color=avg_color
            )
            embed.add_field(name="Emoji", value=f"{new_emoji}", inline=True)
            embed.add_field(name="Nome do Emoji", value=f"```{new_emoji.name}```", inline=True)
            embed.add_field(name="ID do Emoji", value=f"```{new_emoji.id}```", inline=True)
            embed.add_field(name="URL do Emoji", value=f"[Clique aqui para ver o emoji]({new_emoji.url})", inline=True)
            embed.set_thumbnail(url=new_emoji.url)
            embed.set_footer(text=f"Adicionado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed)

        except Exception as e:
            print(e)
            embed = discord.Embed(
                title="⚠️ Erro",
                description="Ocorreu um erro ao adicionar o emoji. Verifique se o nome do emoji ou o ID está correto e tente novamente.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)

    @bot.tree.command(name='addemoji', description='Adiciona um emoji no servidor')
    @commands.has_permissions(manage_emojis=True)
    async def add_emoji(interaction: discord.Interaction, emoji: str):
        try:
            emoji_id = None
            emoji_name = None

            if emoji.startswith('<:') and emoji.endswith('>'):
                emoji_id = emoji.split(':')[2][:-1]
            elif emoji.startswith('<a:') and emoji.endswith('>'):
                emoji_id = emoji.split(':')[2][:-1]
            elif emoji.startswith(':') and emoji.endswith(':'):
                emoji_name = emoji.strip(':')
            else:
                embed = discord.Embed(
                    title="🚫 Erro",
                    description="Por favor, forneça um nome de emoji válido no formato `:nome_do_emoji:` ou um emoji com ID no formato `<:emoji_nome:emoji_id>`.",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
                return

            emoji_to_add = None

            if emoji_id:
                for guild in bot.guilds:
                    emoji_to_add = discord.utils.get(guild.emojis, id=int(emoji_id))
                    if emoji_to_add:
                        break
            elif emoji_name:
                for guild in bot.guilds:
                    emoji_to_add = discord.utils.get(guild.emojis, name=emoji_name)
                    if emoji_to_add:
                        break

            if not emoji_to_add:
                embed = discord.Embed(
                    title="🚫 Emoji Não Encontrado",
                    description=f"O emoji `{emoji}` não foi encontrado em nenhum servidor onde o bot está presente.",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
                return

            emoji_url = str(emoji_to_add.url)
            avg_color, image_bytes = await get_image_color(emoji_url)

            guild = interaction.guild

            if len(guild.emojis) >= guild.emoji_limit:
                embed = discord.Embed(
                    title="⚠️ Limite de Emojis Atingido",
                    description="O servidor já atingiu o limite máximo de emojis.",
                    color=discord.Color.red()
                )
                embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
                return

            existing_emoji = discord.utils.get(guild.emojis, name=emoji_to_add.name)
            if existing_emoji:
                await existing_emoji.delete()

            new_emoji = await guild.create_custom_emoji(name=emoji_to_add.name, image=image_bytes)

            embed = discord.Embed(
                title="✅ Emoji Adicionado com Sucesso!",
                description=f"O emoji `{new_emoji.name}` foi adicionado ao servidor com sucesso!",
                color=avg_color
            )
            embed.add_field(name="Emoji", value=f"{new_emoji}", inline=True)
            embed.add_field(name="Nome do Emoji", value=f"```{new_emoji.name}```", inline=True)
            embed.add_field(name="ID do Emoji", value=f"```{new_emoji.id}```", inline=True)
            embed.add_field(name="URL do Emoji", value=f"[Clique aqui para ver o emoji]({new_emoji.url})", inline=True)
            embed.set_thumbnail(url=new_emoji.url)
            embed.set_footer(text=f"Adicionado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(e)
            embed = discord.Embed(
                title="⚠️ Erro",
                description="Ocorreu um erro ao adicionar o emoji. Verifique se o nome do emoji ou o ID está correto e tente novamente.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
