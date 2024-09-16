import discord
from discord.ext import commands
from pyzbar.pyzbar import decode
from PIL import Image, ExifTags
import requests
import tempfile
import os

def setup_qrscan(bot):
    @bot.command(name='qrscan', help='Escaneia um QR code e mostra as informações. Uso: L.qrscan <anexo/url>')
    async def qrscan(ctx, url_or_attachment: str = None):
        def scan_qr(image_path):
            image = Image.open(image_path)
            decoded_objects = decode(image)
            return decoded_objects, image
        
        def extract_metadata(image):
            metadata = {}
            if hasattr(image, '_getexif'):
                exifdata = image._getexif()
                if exifdata:
                    for tag, value in exifdata.items():
                        tag_name = ExifTags.TAGS.get(tag, tag)
                        metadata[tag_name] = value
            return metadata
        
        if not url_or_attachment and not ctx.message.attachments:
            await ctx.reply("Por favor, forneça uma URL ou um anexo de imagem contendo o QR code.")
            return

        loading_message = await ctx.reply("```Escaneando QR code... ⏳```")
        
        image_path = None

        if url_or_attachment:
            try:
                response = requests.get(url_or_attachment, stream=True)
                if response.status_code == 200:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
                        for chunk in response.iter_content(1024):
                            temp.write(chunk)
                        image_path = temp.name
                else:
                    await loading_message.delete()
                    await ctx.reply("Não foi possível baixar a imagem da URL fornecida.")
                    return
            except Exception as e:
                await loading_message.delete()
                await ctx.reply(f"Erro ao baixar a imagem: {str(e)}")
                return

        elif ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment.content_type.startswith('image'):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
                    await attachment.save(temp.name)
                    image_path = temp.name
            else:
                await loading_message.delete()
                await ctx.reply("Por favor, forneça um anexo de imagem válido contendo o QR code.")
                return
        
        decoded_objects, image = scan_qr(image_path)
        
        await loading_message.delete()
        
        if not decoded_objects:
            await ctx.reply("Nenhum QR code válido encontrado na imagem fornecida.")
            return
        
        results = []
        for obj in decoded_objects:
            results.append(f"Tipo: {obj.type}\nDados: {obj.data.decode('utf-8')}\n")
        
        result_text = "\n".join(results)

        metadata = extract_metadata(image)
        metadata_text = "\n".join([f"{key}: {value}" for key, value in metadata.items()])

        thumbnail_path = None
        if decoded_objects:
            thumbnail_path = image_path
        
        embed = discord.Embed(
            title="QR Code Scan",
            description=result_text,
            color=discord.Color.blue()
        )
        embed.add_field(name="Metadados da Imagem", value=metadata_text if metadata_text else "Nenhum metadado encontrado", inline=False)
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        
        if thumbnail_path:
            file = discord.File(thumbnail_path, filename="thumbnail.png")
            embed.set_thumbnail(url="attachment://thumbnail.png")
            await ctx.reply(embed=embed, file=file)
            os.remove(thumbnail_path)
        else:
            await ctx.reply(embed=embed)
        
        if image_path and os.path.exists(image_path):
            os.remove(image_path)



    @bot.tree.command(name='qrscan', description='Escaneia um QR code e mostra as informações.')
    async def qrscan(interaction: discord.Interaction, url: str = None):
        def scan_qr(image_path):
            image = Image.open(image_path)
            decoded_objects = decode(image)
            return decoded_objects, image
        
        def extract_metadata(image):
            metadata = {}
            if hasattr(image, '_getexif'):
                exifdata = image._getexif()
                if exifdata:
                    for tag, value in exifdata.items():
                        tag_name = ExifTags.get(tag, tag)
                        metadata[tag_name] = value
            return metadata
        
        if not url_or_attachment and not interaction.message.attachments:
            await interaction.response.send_message("Por favor, forneça uma URL ou um anexo de imagem contendo o QR code.", ephemeral=True)
            return

        image_path = None

        if url_or_attachment:
            try:
                response = requests.get(url_or_attachment, stream=True)
                if response.status_code == 200:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
                        for chunk in response.iter_content(1024):
                            temp.write(chunk)
                        image_path = temp.name
                else:
                    await interaction.response.send_message("Não foi possível baixar a imagem da URL fornecida.", ephemeral=True)
                    return
            except Exception as e:
                await interaction.response.send_message(f"Erro ao baixar a imagem: {str(e)}", ephemeral=True)
                return

        elif interaction.message.attachments:
            attachment = interaction.message.attachments[0]
            if attachment.content_type.startswith('image'):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
                    await attachment.save(temp.name)
                    image_path = temp.name
            else:
                await interaction.response.send_message("Por favor, forneça um anexo de imagem válido contendo o QR code.", ephemeral=True)
                return
        
        decoded_objects, image = scan_qr(image_path)
        
        
        if not decoded_objects:
            await interaction.response.send_message("Nenhum QR code válido encontrado na imagem fornecida.", ephemeral=True)
            return
        
        results = [f"Tipo: {obj.type}\nDados: {obj.data.decode('utf-8')}\n" for obj in decoded_objects]
        result_text = "\n".join(results)

        metadata = extract_metadata(image)
        metadata_text = "\n".join([f"{key}: {value}" for key, value in metadata.items()])

        embed = discord.Embed(
            title="QR Code Scan",
            description=result_text,
            color=discord.Color.blue()
        )
        embed.add_field(name="Metadados da Imagem", value=metadata_text if metadata_text else "Nenhum metadado encontrado", inline=False)
        embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
        
        if image_path:
            file = discord.File(image_path, filename="thumbnail.png")
            embed.set_thumbnail(url="attachment://thumbnail.png")
            await interaction.response.send_message(embed=embed, file=file)
            os.remove(image_path)
        else:
            await interaction.response.send_message(embed=embed)
        
        if image_path and os.path.exists(image_path):
            os.remove(image_path)