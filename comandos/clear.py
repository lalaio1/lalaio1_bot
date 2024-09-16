import discord
import os
import hashlib
from discord.ext import commands
from discord.ui import Button, View

class ClearMessagesView(View):
    def __init__(self, deleted_messages):
        super().__init__()
        self.deleted_messages = deleted_messages

    @discord.ui.button(label="Baixar Mensagens Apagadas 🚮", style=discord.ButtonStyle.blurple)
    async def download_button_callback(self, interaction: discord.Interaction, button: Button):
        try:
            message_list = []
            for message in self.deleted_messages:
                timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                content = message.content.replace("\n", " ")
                author = f"{message.author.name}#{message.author.discriminator} (ID: {message.author.id})"
                message_list.append(f"[{timestamp}] {author}: {content}")

            full_info = "\n".join(message_list)

            # Gera uma hash SHA256 a partir do conteúdo das mensagens deletadas
            hash_object = hashlib.sha256(full_info.encode())
            hex_dig = hash_object.hexdigest()

            # Define o caminho do arquivo com a hash como nome
            file_dir = "./temp/clear/"
            os.makedirs(file_dir, exist_ok=True)
            file_path = os.path.join(file_dir, f"{hex_dig}.txt")

            # Salva o conteúdo no arquivo
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(full_info)

            # Envia o arquivo como resposta no Discord
            await interaction.response.send_message(file=discord.File(file_path), ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Baixar Mensagens",
                description=f"Ocorreu um erro ao tentar baixar as mensagens: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

def setup_clear(bot):
    @bot.command(name='clear', help='Exclui mensagens do canal atual')
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int):
        deleted = await ctx.channel.purge(limit=amount + 1)
        deleted_count = len(deleted) - 1 

        if deleted_count > 0:
            view = ClearMessagesView(deleted)
            await ctx.send(embed=generate_clear_embed(deleted_count, ctx.author), view=view)
        else:
            await ctx.send(embed=generate_clear_embed(deleted_count, ctx.author))

    @clear.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Sem Permissão",
                description="Você não tem permissão suficiente para usar este comando.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    def generate_clear_embed(deleted_count, member):
        embed = discord.Embed(title="🗑️ Mensagens Excluídas", color=discord.Color.red())
        embed.add_field(name="Total de Mensagens Excluídas", value=deleted_count, inline=False)
        embed.set_footer(text=f"Comando executado por {member.name}#{member.discriminator}", icon_url=member.avatar.url)
        return embed

    @bot.command(name='clear_all', help='Limpa todas as mensagens do chat')
    @commands.has_permissions(manage_messages=True)
    async def clear_all(ctx):
        deleted_messages = []
        deleted_count = 0
        while True:
            deleted = await ctx.channel.purge(limit=100)
            if len(deleted) == 0:
                break
            deleted_messages.extend(deleted)
            deleted_count += len(deleted)
        
        if deleted_count > 0:
            view = ClearMessagesView(deleted_messages)
            await ctx.send(embed=generate_clear_all_embed(deleted_count, ctx.author), view=view)
        else:
            await ctx.send(embed=generate_clear_all_embed(deleted_count, ctx.author))

    @clear_all.error
    async def clear_all_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Sem Permissão",
                description="Você não tem permissão suficiente para usar este comando.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    def generate_clear_all_embed(deleted_count, member):
        embed = discord.Embed(title="🗑️ Mensagens Excluídas", color=discord.Color.red())
        embed.add_field(name="Total de Mensagens Excluídas", value=deleted_count, inline=False)
        embed.set_footer(text=f"Comando executado por {member.name}#{member.discriminator}", icon_url=member.avatar.url)
        return embed

    @bot.tree.command(name='clear', description='Exclui mensagens do canal atual.')
    @commands.has_permissions(manage_messages=True)
    async def tree_clear(interaction: discord.Interaction, amount: int):
        deleted = await interaction.channel.purge(limit=amount + 1)
        deleted_count = len(deleted) - 1 

        if deleted_count > 0:
            view = ClearMessagesView(deleted)
            await interaction.response.send_message(embed=generate_clear_embed(deleted_count, interaction.user), view=view)
        else:
            await interaction.response.send_message(embed=generate_clear_embed(deleted_count, interaction.user))

    @tree_clear.error
    async def tree_clear_error(interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Sem Permissão",
                description="Você não tem permissão suficiente para usar este comando.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name='clear_all', description='Limpa todas as mensagens do chat.')
    @commands.has_permissions(manage_messages=True)
    async def tree_clear_all(interaction: discord.Interaction):
        deleted_messages = []
        deleted_count = 0
        while True:
            deleted = await interaction.channel.purge(limit=100)
            if len(deleted) == 0:
                break
            deleted_messages.extend(deleted)
            deleted_count += len(deleted)
        
        if deleted_count > 0:
            view = ClearMessagesView(deleted_messages)
            await interaction.response.send_message(embed=generate_clear_all_embed(deleted_count, interaction.user), view=view)
        else:
            await interaction.response.send_message(embed=generate_clear_all_embed(deleted_count, interaction.user))

    @tree_clear_all.error
    async def tree_clear_all_error(interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Sem Permissão",
                description="Você não tem permissão suficiente para usar este comando.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
