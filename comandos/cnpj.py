import discord
import re
import requests

def setup_cnpj(bot):
    @bot.command('cnpj', help='busca informações sobre um cnpj')
    async def cnpj(ctx, ip):
        if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', ip) and not re.match(r'^\d{14}$', ip):
            embed = discord.Embed(
                title = '⚠️ | ERRO DE FORMATO DE CNPJ!',
                description = 'O CNPJ fornecido parece estar em um formato incorreto. Deve ser algo como 12.345.678/0001-95 ou 12345678000195.',
                color = discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        ip = re.sub('[^0-9]', '', ip)

        url = requests.get('https://www.receitaws.com.br/v1/cnpj/' + ip)
        req = url.json()

        if 'erro' in req:
            embed = discord.Embed(
                title = '⚠️ | ERRO DE CNPJ NÃO ENCONTRADO!',
                description = 'Desculpe, não consegui encontrar informações para o CNPJ fornecido. Por favor, verifique se ele está correto.',
                color = discord.Color.red()
            )
            await ctx.reply(embed=embed)
        else:
            maps_url2 = f'https://www.google.com/maps/search/?api=1&query={req["logradouro"].replace(" ", "+")},{req["municipio"].replace(" ", "+")},{req["uf"]}'

            embed = discord.Embed(
                title = '🔎 | CNPJ ENCONTRADO!',
                description = f'📅 •  ABERTURA: {req["abertura"]}\n🔍 •  SITUAÇÃO: {req["situacao"]}\n📁 •  TIPO: {req["tipo"]}\n📝 •  NOME: {req["nome"]}\n🎭 •  FANTASIA: {req["fantasia"]}\n🏢 •  PORTE: {req["porte"]}\n⚖️ •  NATUREZA JURÍDICA: {req["natureza_juridica"]}\n🛣️ •  LOGRADOURO: {req["logradouro"]}\n🔢 •  NÚMERO: {req["numero"]}\n🏙️ •  MUNICÍPIO: {req["municipio"]}\n🏘️ •  BAIRRO: {req["bairro"]}\n🗺️ •  ESTADO: {req["uf"]}\n📬 •  CEP: {req["cep"]}\n📞 •  TELEFONE: {req["telefone"]}\n📅 •  DT SITUAÇÃO: {req["data_situacao"]}\n❓ •  MOTIVO: {req["motivo_situacao"]}\n💼 •  CNPJ: {req["cnpj"]}\n🔄 •  ÚLTIMA ATUALIZAÇÃO: {req["ultima_atualizacao"]}\n📍 •  Google Maps {maps_url2}',
                color = discord.Color.blue()
            )

            await ctx.reply(embed=embed)

    @bot.tree.command(name='cnpj', description='Busca informações sobre um CNPJ')
    async def cnpj(interaction: discord.Interaction, cnpj: str):
        # Verificação do formato do CNPJ
        if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', cnpj) and not re.match(r'^\d{14}$', cnpj):
            embed = discord.Embed(
                title='⚠️ | ERRO DE FORMATO DE CNPJ!',
                description='O CNPJ fornecido parece estar em um formato incorreto. Deve ser algo como 12.345.678/0001-95 ou 12345678000195.',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Remoção de caracteres não numéricos do CNPJ
        cnpj = re.sub('[^0-9]', '', cnpj)

        # Consulta à API da Receita WS
        url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
        response = requests.get(url)
        req = response.json()

        # Tratamento da resposta da API
        if 'erro' in req:
            embed = discord.Embed(
                title='⚠️ | ERRO DE CNPJ NÃO ENCONTRADO!',
                description='Desculpe, não consegui encontrar informações para o CNPJ fornecido. Por favor, verifique se ele está correto.',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            maps_url = f'https://www.google.com/maps/search/?api=1&query={req["logradouro"].replace(" ", "+")},{req["municipio"].replace(" ", "+")},{req["uf"]}'

            embed = discord.Embed(
                title='🔎 | CNPJ ENCONTRADO!',
                description=(
                    f'📅 • ABERTURA: {req["abertura"]}\n'
                    f'🔍 • SITUAÇÃO: {req["situacao"]}\n'
                    f'📁 • TIPO: {req["tipo"]}\n'
                    f'📝 • NOME: {req["nome"]}\n'
                    f'🎭 • FANTASIA: {req["fantasia"]}\n'
                    f'🏢 • PORTE: {req["porte"]}\n'
                    f'⚖️ • NATUREZA JURÍDICA: {req["natureza_juridica"]}\n'
                    f'🛣️ • LOGRADOURO: {req["logradouro"]}\n'
                    f'🔢 • NÚMERO: {req["numero"]}\n'
                    f'🏙️ • MUNICÍPIO: {req["municipio"]}\n'
                    f'🏘️ • BAIRRO: {req["bairro"]}\n'
                    f'🗺️ • ESTADO: {req["uf"]}\n'
                    f'📬 • CEP: {req["cep"]}\n'
                    f'📞 • TELEFONE: {req["telefone"]}\n'
                    f'📅 • DT SITUAÇÃO: {req["data_situacao"]}\n'
                    f'❓ • MOTIVO: {req["motivo_situacao"]}\n'
                    f'💼 • CNPJ: {req["cnpj"]}\n'
                    f'🔄 • ÚLTIMA ATUALIZAÇÃO: {req["ultima_atualizacao"]}\n'
                    f'📍 • [Google Maps]({maps_url})'
                ),
                color=discord.Color.blue()
            )

            await interaction.response.send_message(embed=embed)