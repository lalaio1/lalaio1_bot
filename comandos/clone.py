import discord
import os
import asyncio
import zipfile
import shutil
from urllib.parse import urlparse

def setup_clone(bot):
    @bot.command(name='clone')
    async def extract(ctx, url: str):
        try:
            # Validar e sanitizar o URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme.startswith('http'):
                raise ValueError("URL inválido. Apenas URLs HTTP/HTTPS são suportados.")

            # Remover o esquema (http:// ou https://) da URL
            netloc = parsed_url.netloc
            output_folder_path = f'./scripts/site_cloner/{netloc}'  # Pasta onde o site será clonado

            # Nome do arquivo ZIP
            zip_filename = "site_cloned.zip"
            zip_filepath = os.path.abspath(os.path.join('.', zip_filename))  # Caminho absoluto para o arquivo ZIP
            script_path = os.path.abspath('./scripts/site_cloner/sitecloner.py')

            embed = discord.Embed(title=f"🧬 Clonagem e Extração de {url}", color=discord.Color.blurple())
            message = await ctx.reply(embed=embed)

            process = await asyncio.create_subprocess_exec(
                'python', script_path, url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd='./scripts/site_cloner'
            )

            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                raise Exception(f"Erro ao executar o script: {stderr.decode()}")

            # Verificar se a pasta foi criada
            if os.path.isdir(output_folder_path):
                num_files = sum(len(files) for _, _, files in os.walk(output_folder_path))

                # Mensagem de arquivos extraídos
                embed.add_field(name="__💌 Arquivos Extraídos__", value=f"```Fix\nForam extraídos {num_files} arquivos.\n```", inline=False)
                await message.edit(embed=embed)

                # Mensagem de compactação em andamento
                await message.edit(embed=discord.Embed(description=f"__📀 Compactando arquivos__\n```Fix\nEm andamento\n```", color=discord.Color.blue()))

                # Compactar apenas arquivos seguros
                with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(output_folder_path):
                        for file in files:
                            # Ignorar arquivos ocultos ou potencialmente sensíveis
                            if file.startswith('.') or file.endswith(('.env', '.ini', '.config')):
                                continue
                            zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), output_folder_path))

                # Verificar se o arquivo ZIP foi criado antes de tentar enviar
                if os.path.exists(zip_filepath):
                    # Mensagem de arquivos compactados
                    await message.edit(embed=discord.Embed(description=f"🎁 Arquivos compactados.\n```Diff\n+ Finalizado!\n```", color=discord.Color.green()))
                    await message.delete()
                    # Enviar o arquivo ZIP
                    await ctx.reply(file=discord.File(zip_filepath))

                    # Informações do arquivo
                    file_info_embed = discord.Embed(
                        title="Informações do Arquivo",
                        color=0x8A2BE2,
                        description=f"```ansi\n[2;35mNome: {zip_filename}\n"
                                    f"Tipo: {zipfile.ZIP_DEFLATED}\n"
                                    f"Tamanho: {os.path.getsize(zip_filepath) / (1024 * 1024):.2f} MB\n[0m```"
                    )
                    file_info_embed.set_thumbnail(url="https://i.ibb.co/QYg0QFc/folder-archive-documents-open-icon-131246.png")

                    await ctx.reply(embed=file_info_embed)

                    shutil.rmtree(output_folder_path)

                    # Remover o arquivo ZIP após o envio
                    os.remove(zip_filepath)

                else:
                    await message.edit(embed=discord.Embed(description=f"O arquivo ZIP '{zip_filepath}' não foi encontrado após a compactação.", color=discord.Color.red()))

            else:
                await message.edit(embed=discord.Embed(description=f"A pasta de saída '{output_folder_path}' não foi encontrada após a clonagem.", color=discord.Color.red()))

        except Exception as e:
            await ctx.reply(embed=discord.Embed(description=f"Ocorreu um erro durante a extração: {str(e)}", color=discord.Color.red()))