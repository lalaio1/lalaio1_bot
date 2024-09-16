import discord
import requests
from discord.ext import commands

def setup_gen(bot):
    @bot.command(name='gen')
    async def generate_user(ctx, country='us'):
        url = f'https://randomuser.me/api/?nat={country}'
        response = requests.get(url)
        data = response.json()
        user = data['results'][0]

        embed = discord.Embed(
            title = '👥 | Usuário Gerado',
            color = discord.Color.blue()
        )
        
        embed.add_field(name='📛 Nome', value=f'{user["name"]["first"]} {user["name"]["last"]}', inline=False)
        embed.add_field(name='⚤ Gênero', value=user['gender'], inline=False)
        embed.add_field(name='🎂 Data de Nascimento', value=user['dob']['date'], inline=False)
        embed.add_field(name='🏠 Endereço', value=f'{user["location"]["street"]["name"]}, {user["location"]["city"]}, {user["location"]["state"]}, {user["location"]["country"]}', inline=False)
        embed.add_field(name='📧 Email', value=user['email'], inline=False)
        embed.add_field(name='☎️ Telefone', value=user['phone'], inline=False)
        embed.add_field(name='📱 Celular', value=user['cell'], inline=False)
        embed.add_field(name='🌐 Nacionalidade', value=user['nat'], inline=False)
        embed.add_field(name='🔑 UUID', value=user['login']['uuid'], inline=False)
        embed.add_field(name='📛 Nome de Usuário', value=user['login']['username'], inline=False)
        embed.add_field(name='🔒 Senha', value=user['login']['password'], inline=False)
        embed.add_field(name='🧂 Salt', value=user['login']['salt'], inline=False)
        embed.add_field(name='🔐 MD5', value=user['login']['md5'], inline=False)
        embed.add_field(name='🔐 SHA1', value=user['login']['sha1'], inline=False)
        embed.add_field(name='🔐 SHA256', value=user['login']['sha256'], inline=False)
        embed.add_field(name='🎂 Data de Registro', value=user['registered']['date'], inline=False)
        embed.add_field(name='🆔 ID', value=user['id']['name'], inline=False)
        
        embed.set_thumbnail(url=user['picture']['large'])
        
        await ctx.reply(embed=embed)


    @bot.tree.command(name='gen', description='Gera um usuário aleatório com base no país especificado.')
    async def gen_slash(interaction: discord.Interaction, country: str = 'us'):
        url = f'https://randomuser.me/api/?nat={country}'
        response = requests.get(url)
        data = response.json()
        user = data['results'][0]

        embed = discord.Embed(
            title='👥 | Usuário Gerado',
            color=discord.Color.blue()
        )
        
        embed.add_field(name='📛 Nome', value=f'{user["name"]["first"]} {user["name"]["last"]}', inline=False)
        embed.add_field(name='⚤ Gênero', value=user['gender'], inline=False)
        embed.add_field(name='🎂 Data de Nascimento', value=user['dob']['date'], inline=False)
        embed.add_field(name='🏠 Endereço', value=f'{user["location"]["street"]["name"]}, {user["location"]["city"]}, {user["location"]["state"]}, {user["location"]["country"]}', inline=False)
        embed.add_field(name='📧 Email', value=user['email'], inline=False)
        embed.add_field(name='☎️ Telefone', value=user['phone'], inline=False)
        embed.add_field(name='📱 Celular', value=user['cell'], inline=False)
        embed.add_field(name='🌐 Nacionalidade', value=user['nat'], inline=False)
        embed.add_field(name='🔑 UUID', value=user['login']['uuid'], inline=False)
        embed.add_field(name='📛 Nome de Usuário', value=user['login']['username'], inline=False)
        embed.add_field(name='🔒 Senha', value=user['login']['password'], inline=False)
        embed.add_field(name='🧂 Salt', value=user['login']['salt'], inline=False)
        embed.add_field(name='🔐 MD5', value=user['login']['md5'], inline=False)
        embed.add_field(name='🔐 SHA1', value=user['login']['sha1'], inline=False)
        embed.add_field(name='🔐 SHA256', value=user['login']['sha256'], inline=False)
        embed.add_field(name='🎂 Data de Registro', value=user['registered']['date'], inline=False)
        embed.add_field(name='🆔 ID', value=user['id']['name'], inline=False)
        
        embed.set_thumbnail(url=user['picture']['large'])
        
        await interaction.response.send_message(embed=embed)