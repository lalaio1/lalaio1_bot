from pathlib import Path
import discord
import json
from discord.ui import Button, View
import asyncio

class PaginatorView(View):
    def __init__(self, pages, user):
        super().__init__(timeout=180)
        self.pages = pages
        self.current_page = 0
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.user

    @discord.ui.button(label="⬅️ Anterior", style=discord.ButtonStyle.primary, disabled=True)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        self.current_page -= 1
        await self.update_page(interaction)

    @discord.ui.button(label="Próxima ➡️", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        self.current_page += 1
        await self.update_page(interaction)

    async def update_page(self, interaction):
        for child in self.children:
            child.disabled = False

        if self.current_page == 0:
            self.previous_page.disabled = True
        if self.current_page == len(self.pages) - 1:
            self.next_page.disabled = True

        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

def setup_help(bot):
    @bot.command(name='help')
    async def help_command(ctx):
        try:
            commands_file_path = Path('json/commands/commands.json')
            
            if not commands_file_path.is_file():
                await ctx.message.reply(
                    embed=discord.Embed(
                        title="❌ Arquivo não encontrado",
                        description="O arquivo `commands.json` não foi encontrado.",
                        color=discord.Color.red()
                    )
                )
                return

            with open(commands_file_path, 'r', encoding='utf-8') as file:
                commands_list = json.load(file)

            chunks = [commands_list[i:i + 3] for i in range(0, len(commands_list), 3)]
            pages = []

            for index, chunk in enumerate(chunks):
                title = "📜 Lista de Comandos" if index == 0 else "📜 Continuação"
                embed = discord.Embed(
                    title=title,
                    description="Aqui estão todos os comandos disponíveis:",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
                embed.set_footer(text=f"Página {index + 1} de {len(chunks)}")
                embed.timestamp = discord.utils.utcnow()

                for command in chunk:
                    examples_formatted = "\n".join([f"`{example}`" for example in command['examples']])
                    embed.add_field(
                        name=f"**{command['name']}**",
                        value=(
                            f"{command['description']}\n"
                            f"**Sintaxe:** `{command['syntax']}`\n"
                            f"**Exemplos:**\n{examples_formatted}"
                        ),
                        inline=False
                    )

                pages.append(embed)

            view = PaginatorView(pages, ctx.author)
            await ctx.reply(embed=pages[0], view=view)

        except Exception as e:
            error_message = await ctx.reply(
                embed=discord.Embed(
                    title="❌ Ocorreu um erro",
                    description=f"Ocorreu um erro: {str(e)}",
                    color=discord.Color.red()
                )
            )
            await asyncio.sleep(20)
            await error_message.delete()






    @bot.tree.command(name='help', description='Mostra uma lista de todos os comandos disponíveis.')
    async def help_slash_command(interaction: discord.Interaction):
        await send_help(interaction, interaction.user)

async def send_help(interaction, user):
    try:
        commands_file_path = Path('commands/commands.json')
        
        if not commands_file_path.is_file():
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Arquivo não encontrado",
                    description="O arquivo `commands.json` não foi encontrado.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

        with open(commands_file_path, 'r', encoding='utf-8') as file:
            commands_list = json.load(file)

        chunks = [commands_list[i:i + 3] for i in range(0, len(commands_list), 3)]
        pages = []

        for index, chunk in enumerate(chunks):
            title = "📜 Lista de Comandos" if index == 0 else "📜 Continuação"
            embed = discord.Embed(
                title=title,
                description="Aqui estão todos os comandos disponíveis:",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            embed.set_footer(text=f"Página {index + 1} de {len(chunks)}")
            embed.timestamp = discord.utils.utcnow()

            for command in chunk:
                examples_formatted = "\n".join([f"`{example}`" for example in command['examples']])
                embed.add_field(
                    name=f"**{command['name']}**",
                    value=(
                        f"{command['description']}\n"
                        f"**Sintaxe:** ```{command['syntax']}```\n"
                        f"**Exemplos:**\n{examples_formatted}"
                    ),
                    inline=False
                )

            pages.append(embed)

        view = PaginatorView(pages, user)
        await interaction.response.send_message(
            embed=pages[0], 
            view=view, 
            ephemeral=True
        )

    except Exception as e:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Ocorreu um erro",
                description=f"Ocorreu um erro: {str(e)}",
                color=discord.Color.red()
            ),
            ephemeral=True
        )