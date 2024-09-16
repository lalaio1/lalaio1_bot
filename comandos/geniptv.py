import aiohttp
import discord
import json




username = 'mark6544'
password = 'card654'


async def generate_iptv():
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content-Type': 'application/json',
        'Origin': 'https://wplay.vip',
        'Referer': 'https://wplay.vip/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.wplay.vip/prod/v2/auth/login",
                json={"username": "mark6544", "password": "card654"},
                headers=headers
            ) as login_response:
                login_data = await login_response.json()

            async with session.post(
                "https://api.wplay.vip/prod/v2/lines/test",
                json={"notes": "", "package_p2p": "667a0f479ab1ca5452bf15ad", "krator_package": "1", "package_iptv": 69},
                headers={**headers, 'Authorization': f'Bearer {login_data["token"]}'}
            ) as create_response:
                create_data = await create_response.json()

        return create_data
    except Exception as err:
        print('Error:', err)
        return None



def setup_geniptv(bot):
    @bot.command(name='geniptv')
    async def gerar_iptv(ctx):
        await ctx.reply("```Fix\nGerando ⏳ \n```")
        iptv_data = await generate_iptv()
        if iptv_data:
            embed = discord.Embed(title="🔗 IPTV Gerado", color=0x90EE90)  # Verde claro
            embed.add_field(name="🌐 Site", value="https://w-play.tv/", inline=False)
            embed.add_field(name="🔑 Login", value=f"```Fix\n{iptv_data['username']}\n```", inline=False)
            embed.add_field(name="🔐 Senha", value=f"```Fix\n{iptv_data['password']}\n```", inline=False)
            embed.add_field(name="ℹ️ Outros Detalhes", value=f"```json\n{json.dumps(iptv_data)}\n```", inline=False)
            embed.set_image(url="https://w-play.tv/wp-content/uploads/2024/04/wplay_logo_wt.webp")
            embed.set_footer(text="📍 Confira mais em https://w-play.tv/ ")
            await ctx.send(embed=embed)
        else:
            await ctx.edit("```Falha ao gerar IPTV.```")

    @bot.tree.command(name='geniptv', description='Gera um IPTV e fornece detalhes.')
    async def geniptv_slash(interaction: discord.Interaction):
        # Gera os dados do IPTV
        iptv_data = await generate_iptv()

        if iptv_data:
            embed = discord.Embed(title="🔗 IPTV Gerado", color=0x90EE90)  # Verde claro
            embed.add_field(name="🌐 Site", value="https://w-play.tv/", inline=False)
            embed.add_field(name="🔑 Login", value=f"```Fix\n{iptv_data['username']}\n```", inline=False)
            embed.add_field(name="🔐 Senha", value=f"```Fix\n{iptv_data['password']}\n```", inline=False)
            embed.add_field(name="ℹ️ Outros Detalhes", value=f"```json\n{json.dumps(iptv_data)}\n```", inline=False)
            embed.set_image(url="https://w-play.tv/wp-content/uploads/2024/04/wplay_logo_wt.webp")
            embed.set_footer(text="📍 Confira mais em https://w-play.tv/ ")
            
            # Envia o embed final
            await interaction.response.send_message(embed=embed)
        else:
            # Envia uma mensagem de falha
            await interaction.response.send_message("```Falha ao gerar IPTV.```")