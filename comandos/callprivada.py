import discord
from discord.ext import commands
import json
import os

call_data_file = r'/home/lalaio1/lalaio1 bot/json/call/call.json'
def save_call_data(data):
    with open(call_data_file, 'w') as f:
        json.dump(data, f, indent=4)

def load_call_data():
    if os.path.exists(call_data_file):
        with open(call_data_file, 'r') as f:
            return json.load(f)
    return {}

def setup_call(bot):    
    @bot.command()
    async def call(ctx, *membros: discord.Member):
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name='🔒 Chamadas Privadas')
        
        if not category:
            category = await guild.create_category('🔒 Chamadas Privadas')

        membros = list(membros)
        if ctx.author not in membros:
            membros.append(ctx.author)
        
        creator_name = ctx.author.display_name
        channel_name = f'ᴄᴀʟʟ ᴘʀɪᴠᴀᴅᴀ ᴅᴇ {creator_name}'

        existing_channel = discord.utils.get(category.channels, name=channel_name)
        
        if existing_channel:
            embed = discord.Embed(
                title="Erro",
                description=f'O canal "{channel_name}" já existe.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False),
                ctx.author: discord.PermissionOverwrite(connect=True, manage_channels=True),
            }
            
            for membro in membros:
                overwrites[membro] = discord.PermissionOverwrite(connect=True)

            channel = await category.create_voice_channel(channel_name, overwrites=overwrites, user_limit=len(membros))
            invite = await channel.create_invite(max_age=300)

            embed = discord.Embed(
                title="Sucesso",
                description=f'Canal de chamada privada "{channel_name}" criado!\n\n🔗 [Clique aqui para entrar na call]({invite.url})',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

            call_data = load_call_data()
            call_data[ctx.author.id] = channel.id
            save_call_data(call_data)

    @bot.command()
    async def deletecall(ctx, *, identifier=None):
        call_data = load_call_data()
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name='🔒 Chamadas Privadas')

        if not category:
            embed = discord.Embed(
                title="Erro",
                description='Categoria "🔒 Chamadas Privadas" não encontrada.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if identifier is None:
            channel_id = call_data.get(str(ctx.author.id))
            if channel_id:
                channel = guild.get_channel(channel_id)
            else:
                channel = None
        else:
            try:
                channel_id = int(identifier)
                channel = guild.get_channel(channel_id)
            except ValueError:
                channel = discord.utils.get(category.channels, name=identifier)

        if channel:
            await channel.delete()
            call_data.pop(str(ctx.author.id), None)
            save_call_data(call_data)
            embed = discord.Embed(
                title="Sucesso",
                description=f'Canal de chamada "{channel.name}" excluído.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erro",
                description=f'Canal não encontrado.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    @bot.command()
    async def addcall(ctx, member: discord.Member):
        call_data = load_call_data()
        guild = ctx.guild
        channel_id = call_data.get(str(ctx.author.id))

        if channel_id:
            channel = guild.get_channel(channel_id)
            if channel:
                # Adiciona o membro e aumenta o limite de usuários
                await channel.set_permissions(member, connect=True)
                new_limit = channel.user_limit + 1
                await channel.edit(user_limit=new_limit)
                
                embed = discord.Embed(
                    title="Sucesso",
                    description=f'{member.display_name} foi adicionado à call "{channel.name}". O novo limite de usuários é {new_limit}.',
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Erro",
                    description='Não foi possível encontrar o canal de chamada.',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erro",
                description='Você não possui uma call privada ativa.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)


    @bot.command()
    async def removecall(ctx, member: discord.Member):
        call_data = load_call_data()
        guild = ctx.guild
        channel_id = call_data.get(str(ctx.author.id))

        if channel_id:
            channel = guild.get_channel(channel_id)
            if channel:
                # Remove o membro e diminui o limite de usuários
                await channel.set_permissions(member, overwrite=None)
                new_limit = max(0, channel.user_limit - 1)
                await channel.edit(user_limit=new_limit)
                
                embed = discord.Embed(
                    title="Sucesso",
                    description=f'{member.display_name} foi removido da call "{channel.name}". O novo limite de usuários é {new_limit}.',
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Erro",
                    description='Não foi possível encontrar o canal de chamada.',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erro",
                description='Você não possui uma call privada ativa.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)