import discord
from discord.ext import commands
from discord.ui import View, Button
import webcolors

# Mapeamento de cores
mapeamento_cores = {
    'preto': 'black',
    'branco': 'white',
    'vermelho': 'red',
    'verde': 'green',
    'azul': 'blue',
    'amarelo': 'yellow',
    'roxo': 'purple',
    'laranja': 'orange',
    'rosa': 'pink',
    'cinza': 'gray',
    'ciano': 'cyan',
    'dourado': 'gold',
    'magenta': 'magenta',
    'turquesa': 'turquoise',
    'turmalina': 'tourmaline',
    'esmeralda': 'emerald',
    'azul bebê': 'baby blue',
    'azul piscina': 'pool blue',
    'rosa quente': 'hot pink',
    'rosa chiclete': 'bubblegum pink',
    'rosa claro': 'light pink',
    'prata': 'silver',
    'bronze': 'bronze',
    'arco-íris': 'rainbow',
    'berge': 'beige',
    'nude': 'nude',
    'gelo': 'ice',
    'vermelho escuro': 'dark red',
    'verde escuro': 'dark green',
    'azul escuro': 'dark blue',
    'roxo escuro': 'dark purple',
    'laranja escuro': 'dark orange',
    'rosa escuro': 'dark pink',
    'cinza escuro': 'dark gray',
    'vermelho claro': 'light red',
    'verde claro': 'light green',
    'azul claro': 'light blue',
    'roxo claro': 'light purple',
    'laranja claro': 'light orange',
    'cinza claro': 'light gray',
    'violeta': 'violet',
    'índigo': 'indigo',
    'castanho-avermelhado': 'maroon',
    'verde-oliva': 'olive',
    'azul-marinho': 'navy',
    'verde-azulado': 'teal',
    'coral': 'coral',
    'lavanda': 'lavender',
    'pêssego': 'peach',
    'menta': 'mint',
    'azul turquesa': 'turquoise blue',
    'lavanda blush': 'lavender blush',
    'pérola': 'pearl',
    'platina': 'platinum',
    'ouro rosa': 'rose gold',
    'carvão': 'charcoal',
    'azul meia-noite': 'midnight blue',
    'azul céu': 'sky blue',
    'azul aço': 'steel blue',
    'cinza ardósia escuro': 'dark slate gray',
    'cinza ardósia': 'slate gray',
    'azul cadete': 'cadet blue',
    'verde pálido': 'pale green',
    'verde primavera': 'spring green',
    'turquesa pálido': 'pale turquoise',
    'azul pálido': 'pale blue',
    'rosa pálido': 'pale pink',
    'ameixa': 'plum',
    'violeta claro': 'light violet',
    'índigo claro': 'light indigo',
    'marrom-avermelhado claro': 'light maroon',
    'verde-oliva claro': 'light olive',
    'azul-marinho claro': 'light navy',
    'verde-azulado claro': 'light teal',
    'coral claro': 'light coral',
    'lavanda clara': 'light lavender',
    'pêssego claro': 'light peach',
    'menta clara': 'light mint',
    'azul turquesa claro': 'light turquoise blue',
    'lavanda blush clara': 'light lavender blush',
    'pérola clara': 'light pearl',
    'platina clara': 'light platinum',
    'ouro rosa claro': 'light rose gold',
    'carvão claro': 'light charcoal'
}

class PaginatorView(View):
    def __init__(self, pages, user):
        super().__init__(timeout=180)
        self.pages = pages
        self.current_page = 0
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.user

    @discord.ui.button(label="Anterior ⬅️", style=discord.ButtonStyle.primary, disabled=True)
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


def setup_embed(bot):
    @bot.command(name='embed', help='Cria um embed com a cor e mensagem especificadas. Uso: A.embed <cor> <mensagem>')
    async def embed(ctx, cor, *, mensagem):
        await handle_embed(ctx, cor, mensagem)

    @bot.tree.command(name='embed', description='Cria um embed com a cor e mensagem especificadas.')
    @discord.app_commands.describe(cor='A cor do embed', mensagem='A mensagem do embed')
    async def embed_slash(interaction: discord.Interaction, cor: str, mensagem: str):
        await handle_embed(interaction, cor, mensagem)

async def handle_embed(ctx_or_interaction, cor, mensagem):
    cor_ingles = mapeamento_cores.get(cor.lower())

    if not cor_ingles:
        cores_disponiveis = list(mapeamento_cores.keys())
        per_page = 10
        pages = []
        for i in range(0, len(cores_disponiveis), per_page):
            embed = discord.Embed(
                title="Cores Disponíveis",
                description="\n".join(cores_disponiveis[i:i+per_page]),
                color=discord.Color.blue()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            pages.append(embed)
        
        view = PaginatorView(pages, ctx_or_interaction.user if isinstance(ctx_or_interaction, discord.Interaction) else ctx_or_interaction.author)
        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=pages[0], view=view)
        else:
            await ctx_or_interaction.reply(embed=pages[0], view=view)
        return

    try:
        cor_discord = discord.Color(int(webcolors.name_to_hex(cor_ingles, spec='css3')[1:], 16))
    except ValueError:
        embed = discord.Embed(
            title="Cor Inválida",
            description="```😑 Cor inválida. Use um nome de cor válido.```",
            color=discord.Color.red()
        )
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.reply(embed=embed)
        return

    embed = discord.Embed(
        description=f'{mensagem}',
        color=cor_discord
    )
    embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")

    if isinstance(ctx_or_interaction, discord.Interaction):
        await ctx_or_interaction.response.send_message(embed=embed)
    else:
        await ctx_or_interaction.message.delete()
        await ctx_or_interaction.send(embed=embed)