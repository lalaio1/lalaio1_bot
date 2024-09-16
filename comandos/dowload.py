import discord
from discord.ext import commands
from pytube import YouTube
import os
import asyncio

def setup_dowload(bot):
    MAX_FILE_SIZE = 8 * 1024 * 1024  # Tamanho máximo do arquivo: 8 MB

    @bot.command(name='ytdown', help='Baixa um vídeo do YouTube. Use A.download <url>')
    async def download(ctx, url: str):
        try:
            await ctx.reply(embed=discord.Embed(
                title='Baixando Vídeo',
                description='Fazendo o download ⏳',
                color=discord.Color.blue()
            ))

            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            
            if not stream:
                await ctx.reply(embed=discord.Embed(
                    title='Erro',
                    description='Não foi possível encontrar um stream de vídeo adequado.',
                    color=discord.Color.red()
                ))
                return

            file_path = f"{yt.title}.mp4"

            progress_embed = discord.Embed(
                title='Baixando vídeo',
                description=f'Baixando: {yt.title}',
                color=discord.Color.blue()
            )
            progress_message = await ctx.reply(embed=progress_embed)

            def progress_function(stream, chunk, bytes_remaining):
                progress = (stream.filesize - bytes_remaining) / stream.filesize
                progress_embed.description = f'Baixando: {yt.title}\nProgresso: {progress * 100:.2f}%'
                loop = asyncio.get_event_loop()
                loop.create_task(progress_message.edit(embed=progress_embed))

            yt.register_on_progress_callback(progress_function)
            stream.download(filename=file_path)

            file_size = os.path.getsize(file_path)
            if file_size <= MAX_FILE_SIZE:
                video_embed = discord.Embed(
                    title=yt.title,
                    description=(
                        f'**Duração:** {yt.length // 60} minutos e {yt.length % 60} segundos\n'
                        f'**Visualizações:** {yt.views:,}'
                    ),
                    color=discord.Color.green()
                )
                video_embed.set_thumbnail(url=yt.thumbnail_url)
                video_embed.set_footer(text='Vídeo baixado com sucesso!')

                await ctx.reply(embed=video_embed, file=discord.File(file_path))
            else:
                await ctx.reply(embed=discord.Embed(
                    title='Erro',
                    description='O vídeo é muito grande para ser enviado pelo Discord.',
                    color=discord.Color.red()
                ))

            os.remove(file_path)

        except Exception as e:
            await ctx.reply(embed=discord.Embed(
                title='Erro',
                description=f'Ocorreu um erro ao baixar o vídeo:\n```{e}```',
                color=discord.Color.red()
            ))
            if os.path.exists(file_path):
                os.remove(file_path)

    @bot.tree.command(name='ytdown', description='Baixa um vídeo do YouTube. Use: /ytdown <url>')
    @discord.app_commands.describe(url='A URL do vídeo do YouTube a ser baixado')
    async def download(interaction: discord.Interaction, url: str):
        try:
            await interaction.response.send_message(embed=discord.Embed(
                title='Baixando Vídeo',
                description='Fazendo o download ⏳',
                color=discord.Color.blue()
            ))

            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            
            if not stream:
                await interaction.followup.send(embed=discord.Embed(
                    title='Erro',
                    description='Não foi possível encontrar um stream de vídeo adequado.',
                    color=discord.Color.red()
                ))
                return

            file_path = f"{yt.title}.mp4"

            progress_embed = discord.Embed(
                title='Baixando vídeo',
                description=f'Baixando: {yt.title}',
                color=discord.Color.blue()
            )
            progress_message = await interaction.followup.send(embed=progress_embed)

            def progress_function(stream, chunk, bytes_remaining):
                progress = (stream.filesize - bytes_remaining) / stream.filesize
                progress_embed.description = f'Baixando: {yt.title}\nProgresso: {progress * 100:.2f}%'
                loop = asyncio.get_event_loop()
                loop.create_task(progress_message.edit(embed=progress_embed))

            yt.register_on_progress_callback(progress_function)
            stream.download(filename=file_path)

            file_size = os.path.getsize(file_path)
            if file_size <= MAX_FILE_SIZE:
                video_embed = discord.Embed(
                    title=yt.title,
                    description=(
                        f'**Duração:** {yt.length // 60} minutos e {yt.length % 60} segundos\n'
                        f'**Visualizações:** {yt.views:,}'
                    ),
                    color=discord.Color.green()
                )
                video_embed.set_thumbnail(url=yt.thumbnail_url)
                video_embed.set_footer(text='Vídeo baixado com sucesso!')

                await interaction.followup.send(embed=video_embed, file=discord.File(file_path))
            else:
                await interaction.followup.send(embed=discord.Embed(
                    title='Erro',
                    description='O vídeo é muito grande para ser enviado pelo Discord.',
                    color=discord.Color.red()
                ))

            os.remove(file_path)

        except Exception as e:
            await interaction.followup.send(embed=discord.Embed(
                title='Erro',
                description=f'Ocorreu um erro ao baixar o vídeo:\n```{e}```',
                color=discord.Color.red()
            ))
            if os.path.exists(file_path):
                os.remove(file_path)