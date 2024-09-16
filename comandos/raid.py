import discord
import os
import subprocess
import asyncio
import platform
import re

def is_valid_token(token):
    if not token or ' ' in token:
        return False

    if len(token) < 16:
        return False

    prohibited_characters = r'[\/,()&]'
    if re.search(prohibited_characters, token):
        return False

    return True

async def run_with_timeout(coro, timeout):
    try:
        return await asyncio.wait_for(coro, timeout)
    except asyncio.TimeoutError:
        raise TimeoutError("O processo levou muito tempo para responder.")

def setup_raid(bot):
    @bot.command()
    async def raid(ctx, *, token):
        if not is_valid_token(token):
            embed_error = discord.Embed(
                title="💔 Erro",
                description="__Token inválido. kkkk__",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed_error)
            return

        user_id = str(ctx.author.id) 
        
        try:
            user = await bot.fetch_user(ctx.author.id)
        except discord.HTTPException:
            embed_error = discord.Embed(
                title="💔 Erro",
                description="__Não foi possível encontrar o usuário.__",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed_error)
            return

        try:
            embed_start = discord.Embed(
                title="💠 Iniciando Raid Bot",
                description="__O Raid Bot está sendo iniciado!.__\n-# ***Você receberá uma mensagem direta com mais detalhes***",
                color=discord.Color.blue()
            )
            await ctx.reply(embed=embed_start)

            embed_notify = discord.Embed(
                title="🔔 Raid Bot Iniciado!",
                description="__O Raid Bot foi iniciado. Acompanhe os detalhes na aba de mensagens diretas.__",
                color=discord.Color.green()
            )
            await user.send(embed=embed_notify)

            script_path = os.path.join("scripts", "raidbot", "raid_bot.py")
            if platform.system() == "Windows":
                process = subprocess.Popen(["python", script_path, token, user_id], shell=False)
            else:  # Linux
                process = subprocess.Popen(["python3", script_path, token, user_id], shell=False)

            async def wait_for_completion():
                await asyncio.sleep(300)  # Espera 5 minutos
                if process.poll() is None:
                    process.terminate()
                    embed_end = discord.Embed(
                        title="🛑 Riad Bot __Encerrado__",
                        description="__O Raid Bot foi encerrado após 5 minutos.__",
                        color=discord.Color.red()
                    )
                    await user.send(embed=embed_end)

            await wait_for_completion()

        except Exception as e:
            embed_error = discord.Embed(
                title="💔 Erro",
                description=f"__Ocorreu um erro durante a execução do comando: {str(e)}__",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed_error)
