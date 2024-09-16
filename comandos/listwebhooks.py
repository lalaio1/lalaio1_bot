import discord
from discord.ext import commands
import tempfile
import os


def setup_listwebhooks(bot):

    @bot.command(name='listwebhooks')
    @commands.has_permissions(manage_webhooks=True)
    async def list_webhooks(ctx):
        try:
            webhooks = await ctx.guild.webhooks()
            if not webhooks:
                embed = discord.Embed(
                    title="📜 Lista de Webhooks",
                    description="Não há webhooks configurados neste servidor.",
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
                await ctx.reply(embed=embed)
                return

            # Cria um arquivo temporário para armazenar a lista de webhooks
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                temp_filename = temp_file.name
                # Escreve a lista de webhooks no arquivo
                for webhook in webhooks:
                    temp_file.write(f"Webhook: {webhook.name}\n".encode())
                    temp_file.write(f"ID: {webhook.id}\n".encode())
                    temp_file.write(f"Canal: <#{webhook.channel_id}>\n".encode())
                    temp_file.write(f"URL: {webhook.url}\n".encode())
                    temp_file.write("\n".encode())
            
            # Envia o arquivo como mensagem no Discord
            with open(temp_filename, "rb") as file:
                await ctx.reply(
                    content="Aqui está a lista de webhooks do servidor:",
                    file=discord.File(file, "webhooks_list.txt")
                )
            
            # Remove o arquivo temporário
            os.remove(temp_filename)

        except Exception as e:
            print(e)
            embed = discord.Embed(
                title="⚠️ Erro",
                description="Ocorreu um erro ao listar os webhooks. Tente novamente mais tarde.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)

    @list_webhooks.error
    async def list_webhooks_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Permissão Negada",
                description="Você não tem permissão para usar este comando. É necessário ter a permissão de gerenciar webhooks.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)

    @bot.tree.command(name='listwebhooks', description='Lista todos os webhooks do servidor.')
    @commands.has_permissions(manage_webhooks=True)
    async def list_webhooks(interaction: discord.Interaction):
        try:
            webhooks = await interaction.guild.webhooks()
            if not webhooks:
                embed = discord.Embed(
                    title="📜 Lista de Webhooks",
                    description="Não há webhooks configurados neste servidor.",
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
                return

            # Cria um arquivo temporário para armazenar a lista de webhooks
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                temp_filename = temp_file.name
                # Escreve a lista de webhooks no arquivo
                for webhook in webhooks:
                    temp_file.write(f"Webhook: {webhook.name}\n".encode())
                    temp_file.write(f"ID: `{webhook.id}`\n".encode())
                    temp_file.write(f"Canal: <#{webhook.channel_id}>\n".encode())
                    temp_file.write(f"URL: {webhook.url}\n".encode())
                    temp_file.write("\n".encode())
            
            # Envia o arquivo como mensagem no Discord
            with open(temp_filename, "rb") as file:
                await interaction.response.send_message(
                    content="Aqui está a lista de webhooks do servidor:",
                    file=discord.File(file, "webhooks_list.txt")
                )
            
            # Remove o arquivo temporário
            os.remove(temp_filename)

        except Exception as e:
            print(e)
            embed = discord.Embed(
                title="⚠️ Erro",
                description="Ocorreu um erro ao listar os webhooks. Tente novamente mais tarde.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @list_webhooks.error
    async def list_webhooks_error(interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Permissão Negada",
                description="Você não tem permissão para usar este comando. É necessário ter a permissão de gerenciar webhooks.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)