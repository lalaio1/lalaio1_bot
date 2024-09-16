import discord
from discord.ext import commands
from datetime import datetime

def setup_avatar(bot):
    @bot.command(name='avatar', help='Mostra o avatar de um membro')
    async def avatar(ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        avatar_url = member.avatar.url
        embed = discord.Embed(
            title=f"Avatar de {member.display_name}",
            description=f"[Clique aqui para abrir o avatar em tamanho real]({avatar_url})",
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow()  
        )
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_image(url=avatar_url)
        embed.add_field(name="ID do Usuário", value=(f'```{member.id}```'), inline=True)
        embed.add_field(name="Nome", value=(f'```{member.display_name}```'), inline=True)
        embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        embed.set_footer(text=f"Comando solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        
        await ctx.reply(embed=embed)

    @bot.tree.command(name='avatar', description='Mostra o avatar de um determinado membro')
    async def avatar_slash(interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        avatar_url = member.avatar.url
        embed = discord.Embed(
            title=f"Avatar de {member.display_name}",
            description=f"[Clique aqui para abrir o avatar em tamanho real]({avatar_url})",
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow()  
        )
        embed.set_author(name=str(interaction.user), icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_image(url=avatar_url)
        embed.add_field(name="ID do Usuário", value=(f'```{member.id}```'), inline=True)
        embed.add_field(name="Nome", value=(f'```{member.display_name}```'), inline=True)
        embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        embed.set_footer(text=f"Comando solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)