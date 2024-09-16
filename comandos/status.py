import requests
import discord

def setup_status(bot):
    @bot.command(name='status', help='Verifica o status de um site. Uso: A.status <URL>')
    async def check_site_status(ctx, url: str):
        try:
            response = requests.get(url, timeout=10)  

            if response.status_code == 200:
                status = "Online ✅"
            else:
                status = "Offline ❌"
            
            ping_ms = int(response.elapsed.total_seconds() * 1000) 

            embed = discord.Embed(
                title=f"🌐 Status de '{url}'",
                description=f"**Status:** {status}\n**Ping:** {ping_ms} ms",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url="https://i.ibb.co/ZJ4TtFv/server.png") 
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await ctx.reply(embed=embed)
        
        except requests.exceptions.RequestException as e:
            await ctx.reply(f"🚫 Erro ao verificar o status do site: {str(e)}")

        except Exception as e:
            await ctx.reply(f"🚫 Ocorreu um erro inesperado: {str(e)}")

    @bot.tree.command(name='status', description='Verifica o status de um site. Uso: A.status <URL>')
    async def check_site_status(interaction: discord.Interaction, url: str):
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                status = "Online ✅"
            else:
                status = "Offline ❌"
            
            ping_ms = int(response.elapsed.total_seconds() * 1000)

            embed = discord.Embed(
                title=f"🌐 Status de '{url}'",
                description=f"**Status:** {status}\n**Ping:** {ping_ms} ms",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url="https://i.ibb.co/ZJ4TtFv/server.png")
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            
            await interaction.response.send_message(embed=embed)
        
        except requests.exceptions.RequestException as e:
            await interaction.response.send_message(f"🚫 Erro ao verificar o status do site: {str(e)}")

        except Exception as e:
            await interaction.response.send_message(f"🚫 Ocorreu um erro inesperado: {str(e)}")