import discord
from discord.ext import commands
from datetime import datetime

def setup_info_user(bot):
    @bot.command(name='info_user')
    async def userinfo(ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"Informações do usuário: {member}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        
        embed.add_field(name="Nome", value=f'```{member.display_name}```', inline=True)
        embed.add_field(name="Discriminador", value=f"```#{member.discriminator}```", inline=True)
        embed.add_field(name="ID", value=f'```{member.id}```', inline=True)
        
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        embed.add_field(name="Cargo mais alto", value=member.top_role.mention, inline=True)
        embed.add_field(name="Entrou no servidor em", value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        
        embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        if member.premium_since:
            embed.add_field(name="Boostando desde", value=member.premium_since.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        
        embed.add_field(name="Número de cargos", value=len(member.roles) - 1, inline=True)
        embed.add_field(name="Cargos", value=" ".join([role.mention for role in member.roles if role.name != "@everyone"]), inline=False)
        
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        
        await ctx.reply(embed=embed)

    @bot.tree.command(name='info_user', description='Mostra informações sobre um usuário')
    async def info_user(interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        
        embed = discord.Embed(
            title=f"Informações do usuário: {member}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        
        embed.add_field(name="Nome", value=f'```{member.display_name}```', inline=True)
        embed.add_field(name="Discriminador", value=f"```#{member.discriminator}```", inline=True)
        embed.add_field(name="ID", value=f'```{member.id}```', inline=True)
        
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        embed.add_field(name="Cargo mais alto", value=member.top_role.mention, inline=True)
        embed.add_field(name="Entrou no servidor em", value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        
        embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        if member.premium_since:
            embed.add_field(name="Boostando desde", value=member.premium_since.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        
        embed.add_field(name="Número de cargos", value=len(member.roles) - 1, inline=True)
        embed.add_field(name="Cargos", value=" ".join([role.mention for role in member.roles if role.name != "@everyone"]), inline=False)
        
        embed.set_footer(text=f"Solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)