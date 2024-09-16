from PIL import Image, ImageDraw, ImageFont
import discord 
import io 
import textwrap

object_keywords = [
    'bola', 'cachorro', 'gato', 'computador', 'floresta', 'lua', 'carro', 'casa', 'pessoa'
]

def setup_txt(bot):
    @bot.command(name='txt', help='Cria e envia uma imagem com texto')
    async def create_custom_image(ctx, width: int = 400, height: int = 200, *, text):
        if not (100 <= width <= 1200 and 100 <= height <= 1200):
            await ctx.reply("As dimensões da imagem devem estar entre 100x100 e 1200x1200 pixels.")
            return

        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default()

        lines = textwrap.wrap(text, width=50)  
        y = 10
        for line in lines:
            draw.text((10, y), line, fill='black', font=font)
            y += 20

        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        file = discord.File(img_bytes, filename='image.png')

        embed = discord.Embed(description='Imagem gerada:', color=discord.Color.green())
        embed.set_image(url='attachment://image.png')

        await ctx.reply(embed=embed, file=file)

    @bot.tree.command(name='txt', description='Cria e envia uma imagem com texto')
    async def create_custom_image(interaction: discord.Interaction, width: int = 400, height: int = 200, text: str = ''):
        if not (100 <= width <= 1200 and 100 <= height <= 1200):
            await interaction.response.send_message("As dimensões da imagem devem estar entre 100x100 e 1200x1200 pixels.", ephemeral=True)
            return

        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default()

        lines = textwrap.wrap(text, width=50)  
        y = 10
        for line in lines:
            draw.text((10, y), line, fill='black', font=font)
            y += 20

        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        file = discord.File(img_bytes, filename='image.png')

        embed = discord.Embed(description='Imagem gerada:', color=discord.Color.green())
        embed.set_image(url='attachment://image.png')

        await interaction.response.send_message(embed=embed, file=file)