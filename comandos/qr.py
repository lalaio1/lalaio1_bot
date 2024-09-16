import io 
import qrcode 
import discord

def setup_qr(bot):
    @bot.command(name='qr')
    async def qr(ctx, url: str):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill='rgb(0,0,0)', back_color='rgb(255,255,255)')

        with io.BytesIO() as output:
            img.save(output, format="PNG")
            output.seek(0)
            file = discord.File(output, 'qr_code.png')

        embed = discord.Embed(
            title="QR Code",
            description=f"Aqui está o seu código QR para a URL: {url}",
            color=discord.Color.blurple()
        )
        embed.set_image(url="attachment://qr_code.png")
        embed.set_footer(text=f"Criado por {ctx.author.display_name} em {ctx.message.created_at.strftime('%d/%m/%Y')}")
        
        await ctx.reply(file=file, embed=embed)



    @bot.tree.command(name='qr', description='Gera um código QR para a URL fornecida.')
    async def qr(interaction: discord.Interaction, url: str):
        # Cria o QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill='rgb(0,0,0)', back_color='rgb(255,255,255)')

        # Salva a imagem em memória
        with io.BytesIO() as output:
            img.save(output, format="PNG")
            output.seek(0)
            file = discord.File(output, 'qr_code.png')

        # Cria o embed
        embed = discord.Embed(
            title="QR Code",
            description=f"Aqui está o seu código QR para a URL: {url}",
            color=discord.Color.blurple()
        )
        embed.set_image(url="attachment://qr_code.png")
        embed.set_footer(text=f"Criado por {interaction.user.display_name} em {interaction.created_at.strftime('%d/%m/%Y')}")
        
        # Envia a resposta
        await interaction.response.send_message(file=file, embed=embed)