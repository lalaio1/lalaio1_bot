import discord
import os 
import subprocess
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.oggopus import OggOpus
from mutagen.wavpack import WavPack
from mutagen.apev2 import APEv2
from moviepy.editor import VideoFileClip

def setup_extrair(bot):
    @bot.command(name='extsonds')
    async def extrair_audio(ctx, url: str):
        try:
            message = await ctx.reply("```Fix\n⏳ Baixando o vídeo\n```")

            video_path = 'video.mp4'
            audio_path = 'audio.mp3'

            result = subprocess.run(['yt-dlp', '-o', video_path, url], capture_output=True, text=True)

            if result.returncode != 0:
                await message.edit(content=f"```Erro ao baixar o vídeo:```\n ```{result.stderr}```")
                return

            await message.edit(content="```Fix\n⌛ Extraindo áudio do vídeo\n```")

            video_clip = VideoFileClip(video_path)
            video_clip.audio.write_audiofile(audio_path)
            video_clip.close()

            audio_info = get_audio_info(audio_path)

            duration_seconds = get_video_duration(video_path)

            embed = discord.Embed(
                title="_🎵 Áudio Extraído_",
                description="Aqui estão as informações do áudio extraído do vídeo fornecido:",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url="https://i.ibb.co/jLm6m0f/iconfinder-musicmelodysoundaudio46-4105535-113849.png")
            embed.add_field(name="Status", value="Sucesso", inline=True)
            embed.add_field(name="Tamanho do Arquivo", value=f"{os.path.getsize(audio_path) / (1024 * 1024):.2f} MB", inline=True)
            embed.add_field(name="Duração", value=f"{duration_seconds:.2f} segundos", inline=True)
            
            if audio_info:
                info_str = "\n".join([f"```{key}: {value}```" for key, value in audio_info.items()])
                embed.add_field(name="Informações", value=info_str, inline=False)

            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")

            await message.edit(content="", embed=embed)
            await ctx.reply(file=discord.File(audio_path))

            os.remove(video_path)
            os.remove(audio_path)

        except Exception as e:
            await ctx.reply(embed=discord.Embed(description=f"Ocorreu um erro durante a extração: {str(e)}", color=discord.Color.red()))

    @bot.tree.command(name='extsonds', description='Extrai áudio de um vídeo')
    async def extsonds_slash(interaction: discord.Interaction, url: str):
        try:
            message = await interaction.response.send_message("```Fix\n⏳ Baixando o vídeo\n```")

            video_path = 'video.mp4'
            audio_path = 'audio.mp3'

            result = subprocess.run(['yt-dlp', '-o', video_path, url], capture_output=True, text=True)

            if result.returncode != 0:
                await message.edit(content=f"```Erro ao baixar o vídeo:```\n ```{result.stderr}```")
                return

            await message.edit(content="```Fix\n⌛ Extraindo áudio do vídeo\n```")

            video_clip = VideoFileClip(video_path)
            video_clip.audio.write_audiofile(audio_path)
            video_clip.close()

            audio_info = get_audio_info(audio_path)

            duration_seconds = get_video_duration(video_path)

            embed = discord.Embed(
                title="_🎵 Áudio Extraído_",
                description="Aqui estão as informações do áudio extraído do vídeo fornecido:",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url="https://i.ibb.co/jLm6m0f/iconfinder-musicmelodysoundaudio46-4105535-113849.png")
            embed.add_field(name="Status", value="Sucesso", inline=True)
            embed.add_field(name="Tamanho do Arquivo", value=f"{os.path.getsize(audio_path) / (1024 * 1024):.2f} MB", inline=True)
            embed.add_field(name="Duração", value=f"{duration_seconds:.2f} segundos", inline=True)
            
            if audio_info:
                info_str = "\n".join([f"```{key}: {value}```" for key, value in audio_info.items()])
                embed.add_field(name="Informações", value=info_str, inline=False)

            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")

            await message.edit(content="", embed=embed)
            await interaction.followup.send(file=discord.File(audio_path))

            os.remove(video_path)
            os.remove(audio_path)

        except Exception as e:
            await interaction.response.send_message(embed=discord.Embed(description=f"Ocorreu um erro durante a extração: {str(e)}", color=discord.Color.red()))

def get_audio_info(audio_path):
    audio_info = {}

    try:
        if audio_path.endswith('.mp3'):
            audio = MP3(audio_path)
        elif audio_path.endswith('.mp4'):
            audio = MP4(audio_path)
        elif audio_path.endswith('.flac'):
            audio = FLAC(audio_path)
        elif audio_path.endswith('.opus'):
            audio = OggOpus(audio_path)
        elif audio_path.endswith('.wv'):
            audio = WavPack(audio_path)
        elif audio_path.endswith('.ape'):
            audio = APEv2(audio_path)
        else:
            return None

        audio_info['Formato'] = audio.mime[0]
        audio_info['Duração'] = f"{audio.info.length:.2f} segundos"
        audio_info['Taxa de Bits'] = f"{audio.info.bitrate / 1000} kbps"
        audio_info['Canais'] = audio.info.channels
        audio_info['Frequência de Amostragem'] = f"{audio.info.sample_rate / 1000} kHz"

        return audio_info

    except Exception as e:
        print(f"Erro ao obter informações do áudio: {str(e)}")
        return None

def get_video_duration(video_path):
    try:
        video_clip = VideoFileClip(video_path)
        duration_seconds = video_clip.duration
        video_clip.close()
        return duration_seconds
    except Exception as e:
        print(f"Erro ao obter a duração do vídeo: {str(e)}")
        return 0.0