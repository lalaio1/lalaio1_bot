from bot.func.prefix import * 
from discord.ext import commands
import discord
from discord import app_commands
from discord.ui import Select, View

intenções = discord.Intents.all() 
intenções.members = False  
intenções.presences = False 

bot = commands.Bot(command_prefix=get_prefix, intents=intenções)
bot.remove_command('help')

@bot.command(name='setprefix', help='Define um novo prefixo para o servidor. Uso: L.setprefix <novo_prefixo>')
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new_prefix: str):
    if len(new_prefix) > 5:  
        embed = discord.Embed(
            title="⚠️ **Prefixo Inválido!**",
            description="**O prefixo deve ter no máximo 5 caracteres.**",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)
        return
    
    prefixes = load_prefixes()
    prefixes[str(ctx.guild.id)] = new_prefix
    save_prefixes(prefixes)
    
    embed = discord.Embed(
        title="🔧 **Prefixo Atualizado!**",
        description=f"**O prefixo do bot foi atualizado para `{new_prefix}` neste servidor.**",
        color=discord.Color.green()
    )
    await ctx.reply(embed=embed)

@setprefix.error
async def setprefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="⚠️ **Permissão Negada!**",
            description="**Você não tem permissão para usar este comando.**",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title="⚠️ **Ocorreu um Erro!**",
            description=f"**Ocorreu um erro inesperado.**\n\n📝 Detalhes do erro: `{error}`",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)


@bot.command(name='resetprefix', help='Redefine o prefixo para o padrão L. neste servidor.')
@commands.has_permissions(administrator=True)
async def resetprefix(ctx):
    prefixes = load_prefixes()
    prefixes.pop(str(ctx.guild.id), None) 
    save_prefixes(prefixes)
    
    embed = discord.Embed(
        title="🔄 **Prefixo Resetado!**",
        description="**O prefixo do bot foi resetado para `L.` neste servidor.**",
        color=discord.Color.green()
    )
    await ctx.reply(embed=embed)

@resetprefix.error
async def resetprefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="⚠️ **Permissão Negada!**",
            description="**Você não tem permissão para usar este comando.**",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title="⚠️ **Ocorreu um Erro!**",
            description=f"**Ocorreu um erro inesperado.**\n\n📝 Detalhes do erro: `{error}`",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)

    

@bot.tree.command(name="setprefix", description="Define um novo prefixo para o servidor.")
@app_commands.describe(new_prefix="Novo prefixo para o servidor (máximo 5 caracteres).")
async def setprefix(interaction: discord.Interaction, new_prefix: str):
    if len(new_prefix) > 5:
        embed = discord.Embed(
            title="⚠️ **Prefixo Inválido!**",
            description="**O prefixo deve ter no máximo 5 caracteres.**",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    prefixes = load_prefixes()
    prefixes[str(interaction.guild.id)] = new_prefix
    save_prefixes(prefixes)
    
    embed = discord.Embed(
        title="🔧 **Prefixo Atualizado!**",
        description=f"**O prefixo do bot foi atualizado para `{new_prefix}` neste servidor.**",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="resetprefix", description="Redefine o prefixo para o padrão L. neste servidor.")
async def resetprefix(interaction: discord.Interaction):
    prefixes = load_prefixes()
    prefixes.pop(str(interaction.guild.id), None)
    save_prefixes(prefixes)
    
    embed = discord.Embed(
        title="🔄 **Prefixo Resetado!**",
        description="**O prefixo do bot foi resetado para `L.` neste servidor.**",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="⚠️ **Permissão Negada!**",
            description="**Você não tem permissão para usar este comando.**",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title="⚠️ **Ocorreu um Erro!**",
            description=f"**Ocorreu um erro inesperado.**\n\n📝 Detalhes do erro: `{error}`",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)

@bot.event
async def on_application_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(
            title="⚠️ **Permissão Negada!**",
            description="**Você não tem permissão para usar este comando.**",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title="⚠️ **Ocorreu um Erro!**",
            description=f"**Ocorreu um erro inesperado.**\n\n📝 Detalhes do erro: `{error}`",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.command(name='whatprefix', help='Mostra o prefixo atual do bot neste servidor.')
async def whatprefix(ctx):
    prefixes = load_prefixes()
    current_prefix = prefixes.get(str(ctx.guild.id), 'L.')  # 'L.' é o prefixo padrão caso não tenha sido definido um novo.
    
    embed = discord.Embed(
        title="ℹ️ **Prefixo Atual**",
        description=f"**O prefixo atual do bot neste servidor é `{current_prefix}`.**",
        color=discord.Color.blue()
    )
    await ctx.reply(embed=embed)

@bot.tree.command(name="whatprefix", description="Mostra o prefixo atual do bot neste servidor.")
async def whatprefix(interaction: discord.Interaction):
    prefixes = load_prefixes()
    current_prefix = prefixes.get(str(interaction.guild.id), 'L.')
    
    embed = discord.Embed(
        title="ℹ️ **Prefixo Atual**",
        description=f"**O prefixo atual do bot neste servidor é `{current_prefix}`.**",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@bot.command(name='whatprefixall', help='Mostra um menu para escolher o servidor e ver o prefixo.')
@commands.has_permissions(administrator=True)
async def whatprefixall(ctx):
    prefixes = load_prefixes()
    
    options = [
        discord.SelectOption(label=guild.name, value=str(guild.id))
        for guild in bot.guilds if str(guild.id) in prefixes
    ]
    
    if not options:
        embed = discord.Embed(
            title="⚠️ **Nenhum Prefixo Personalizado!**",
            description="**Não há servidores com prefixos personalizados.**",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)
        return
    
    select = Select(
        placeholder="Selecione um servidor...",
        options=options,
    )
    
    async def select_callback(interaction):
        guild_id = select.values[0]
        guild = next(g for g in bot.guilds if str(g.id) == guild_id)
        current_prefix = prefixes.get(guild_id, 'L.')
        banner_url = guild.banner.url if guild.banner else None
        
        embed = discord.Embed(
            title=f"ℹ️ **Prefixo do Servidor: {guild.name}**",
            description=f"**O prefixo atual do bot neste servidor é `{current_prefix}`.**",
            color=discord.Color.blue()
        )
        
        if banner_url:
            embed.set_image(url=banner_url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    select.callback = select_callback

    view = View()
    view.add_item(select)

    embed = discord.Embed(
        title="📜 **Escolha um Servidor**",
        description="**Selecione um servidor para ver o prefixo atual configurado.**",
        color=discord.Color.green()
    )
    await ctx.reply(embed=embed, view=view)

@bot.tree.command(name="whatprefixall", description="Mostra um menu para escolher o servidor e ver o prefixo.")
async def whatprefixall(interaction: discord.Interaction):
    prefixes = load_prefixes()
    
    options = [
        discord.SelectOption(label=guild.name, value=str(guild.id))
        for guild in bot.guilds if str(guild.id) in prefixes
    ]
    
    if not options:
        embed = discord.Embed(
            title="⚠️ **Nenhum Prefixo Personalizado!**",
            description="**Não há servidores com prefixos personalizados.**",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    select = Select(
        placeholder="Selecione um servidor...",
        options=options,
    )
    
    async def select_callback(interaction: discord.Interaction):
        guild_id = select.values[0]
        guild = next(g for g in bot.guilds if str(g.id) == guild_id)
        current_prefix = prefixes.get(guild_id, 'L.')
        banner_url = guild.banner.url if guild.banner else None
        
        embed = discord.Embed(
            title=f"ℹ️ **Prefixo do Servidor: {guild.name}**",
            description=f"**O prefixo atual do bot neste servidor é `{current_prefix}`.**",
            color=discord.Color.blue()
        )
        
        if banner_url:
            embed.set_image(url=banner_url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    select.callback = select_callback

    view = View()
    view.add_item(select)

    embed = discord.Embed(
        title="📜 **Escolha um Servidor**",
        description="**Selecione um servidor para ver o prefixo atual configurado.**",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=view)
