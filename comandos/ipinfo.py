import discord
import requests
import hashlib
import os
from discord.ui import Button, View


class IPInfoView(View):
    def __init__(self, data_ipinfo, data_ipapi):
        super().__init__()
        self.data_ipinfo = data_ipinfo
        self.data_ipapi = data_ipapi

    @discord.ui.button(label="Informações Completas 🔎", style=discord.ButtonStyle.blurple)
    async def download_button_callback(self, interaction: discord.Interaction, button: Button):
        try:
            loc = self.data_ipinfo.get('loc', 'N/A')
            loc_parts = loc.split(',') if loc != 'N/A' else ['N/A', 'N/A']

            info_list = [
                f"IP: {self.data_ipinfo.get('ip', 'N/A')}",
                f"Versão do IP: {self.data_ipinfo.get('ip_version', 'N/A')}",
                f"City: {self.data_ipinfo.get('city', 'N/A')}",
                f"Região: {self.data_ipinfo.get('region', 'N/A')}",
                f"País: {self.data_ipinfo.get('country', 'N/A')}",
                f"Código Postal: {self.data_ipinfo.get('postal', 'N/A')}",
                f"Latitude: {loc_parts[0]}",
                f"Longitude: {loc_parts[1]}",
                f"ISP: {self.data_ipinfo.get('org', 'N/A')}",
                f"ASN: {self.data_ipinfo.get('asn', 'N/A')}",
                f"Organização: {self.data_ipinfo.get('org', 'N/A')}",
                f"Código da Área: {self.data_ipinfo.get('region', 'N/A')}",
                f"População: {self.data_ipapi.get('population', 'N/A')}",
                f"GMT Offset: {self.data_ipapi.get('utc_offset', 'N/A')}",
                f"Horário Local: {self.data_ipapi.get('timezone', 'N/A')}",
                f"Moeda: {self.data_ipapi.get('currency', 'N/A')}",
                f"Linguagem: {self.data_ipapi.get('languages', 'N/A')}",
                f"Prefixo do Telefone: {self.data_ipapi.get('country_calling_code', 'N/A')}",
                f"Continente: {self.data_ipapi.get('continent', 'N/A')}",
                f"VPN: {self.data_ipapi.get('is_vpn', 'N/A')}",
                f"Proxy: {self.data_ipapi.get('is_proxy', 'N/A')}",
                f"Tor: {self.data_ipapi.get('is_tor', 'N/A')}",
                f"Residencial: {self.data_ipapi.get('is_residential', 'N/A')}",
                f"Móvel: {self.data_ipapi.get('is_mobile', 'N/A')}",
                f"Anycast: {self.data_ipapi.get('is_anycast', 'N/A')}",
                f"Proxy Anônimo: {self.data_ipapi.get('is_anonymous_proxy', 'N/A')}\n"
            ]
            full_info = "\n".join(info_list)

            # Gerar um nome de arquivo único
            ip_hash = hashlib.md5(self.data_ipinfo.get('ip', 'unknown').encode()).hexdigest()
            file_path = f"./temp/ipinfo/{ip_hash}.txt"

            # Certificar-se de que o diretório existe
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Salvar o arquivo
            with open(file_path, "w") as file:
                file.write(full_info)
                
            await interaction.response.send_message(file=discord.File(file_path), ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Buscar Informações",
                description=f"Ocorreu um erro ao tentar buscar as informações: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


def setup_ipinfo(bot):
    @bot.command()
    async def ipinfo(ctx, ip_address):
        try:
            response_ipinfo = requests.get(f"https://ipinfo.io/{ip_address}/json")
            data_ipinfo = response_ipinfo.json()

            response_ipapi = requests.get(f"https://ipapi.co/{ip_address}/json/")
            data_ipapi = response_ipapi.json()

            basic_info_list = [
                f"🌐 IP: {data_ipinfo.get('ip', 'N/A')}",
                f"🏙️ City: {data_ipinfo.get('city', 'N/A')}",
                f"🌍 Região: {data_ipinfo.get('region', 'N/A')}",
                f"🌎 País: {data_ipinfo.get('country', 'N/A')}",
                f"💼 ISP: {data_ipinfo.get('org', 'N/A')}"
            ]

            embed = discord.Embed(title="Informações de IP", color=discord.Color.blue())
            for info in basic_info_list:
                embed.add_field(name="\u200b", value=f"```Fix\n{info}```", inline=False)
            embed.set_footer(text=f"Solicitado por {ctx.author}")

            view = IPInfoView(data_ipinfo, data_ipapi)
            await ctx.reply(embed=embed, view=view)

        except Exception as e:
            print(e)
            error_embed = discord.Embed(title="Erro ao obter informações do IP", color=discord.Color.red())
            error_embed.add_field(name="Detalhes do Erro", value=str(e))
            await ctx.reply(embed=error_embed)

    @bot.tree.command(name='ipinfo', description='Obtém informações sobre um IP.')
    async def ipinfo(interaction: discord.Interaction, ip_address: str):
        try:
            response_ipinfo = requests.get(f"https://ipinfo.io/{ip_address}/json")
            data_ipinfo = response_ipinfo.json()

            response_ipapi = requests.get(f"https://ipapi.co/{ip_address}/json/")
            data_ipapi = response_ipapi.json()

            basic_info_list = [
                f"🌐 IP: {data_ipinfo.get('ip', 'N/A')}",
                f"🏙️ City: {data_ipinfo.get('city', 'N/A')}",
                f"🌍 Região: {data_ipinfo.get('region', 'N/A')}",
                f"🌎 País: {data_ipinfo.get('country', 'N/A')}",
                f"💼 ISP: {data_ipinfo.get('org', 'N/A')}"
            ]

            embed = discord.Embed(title="Informações de IP", color=discord.Color.blue())
            for info in basic_info_list:
                embed.add_field(name="\u200b", value=f"```Fix\n{info}```", inline=False)
            embed.set_footer(text=f"Solicitado por {interaction.user}")

            view = IPInfoView(data_ipinfo, data_ipapi)
            await interaction.response.send_message(embed=embed, view=view)

        except Exception as e:
            print(e)
            error_embed = discord.Embed(title="Erro ao obter informações do IP", color=discord.Color.red())
            error_embed.add_field(name="Detalhes do Erro", value=str(e))
            await interaction.response.send_message(embed=error_embed)
