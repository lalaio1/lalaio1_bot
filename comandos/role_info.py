import discord
from datetime import datetime

def setup_role_info(bot):
    @bot.command(name='role_info')
    async def roleinfo(ctx, role: discord.Role):
        permissions = ', '.join([str(p[0]).replace('_', ' ').title() for p in role.permissions if p[1]])
        if not permissions:
            permissions = "Nenhuma permissão"

        embed = discord.Embed(
            title=f"Informações do cargo: {role.name}",
            color=role.color,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        embed.add_field(name="Nome", value=f'```{role.name}```', inline=True)
        embed.add_field(name="ID", value=f'```{role.id}```', inline=True)
        embed.add_field(name="Cor", value=str(f'```{role.color}```'), inline=True)
        embed.add_field(name="Permissões", value=f'```json\n{permissions}\n```', inline=False)
        embed.add_field(name="Posição", value=role.position, inline=True)
        embed.add_field(name="Mencionável", value="Sim" if role.mentionable else "Não", inline=True)
        embed.add_field(name="Gerenciável", value="Sim" if role.managed else "Não", inline=True)
        embed.add_field(name="Membros com este cargo", value=len(role.members), inline=True)
        embed.add_field(name="Cargo padrão", value="Sim" if role.is_default() else "Não", inline=True)
        embed.add_field(name="Cargo de integração", value="Sim" if role.is_integration() else "Não", inline=True)
        embed.add_field(name="Cargo de boost", value="Sim" if role.is_premium_subscriber() else "Não", inline=True)
        embed.add_field(name="Criado em", value=role.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        
        await ctx.reply(embed=embed)

    @bot.tree.command(name='role_info', description='Mostra informações detalhadas sobre um cargo.')
    async def role_info(interaction: discord.Interaction, role: discord.Role):
        permissions = ', '.join([str(p[0]).replace('_', ' ').title() for p in role.permissions if p[1]])
        if not permissions:
            permissions = "Nenhuma permissão"

        embed = discord.Embed(
            title=f"Informações do cargo: {role.name}",
            color=role.color,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        
        embed.add_field(name="Nome", value=f'```{role.name}```', inline=True)
        embed.add_field(name="ID", value=f'```{role.id}```', inline=True)
        embed.add_field(name="Cor", value=str(f'```{role.color}```'), inline=True)
        embed.add_field(name="Permissões", value=f'```json\n{permissions}\n```', inline=False)
        embed.add_field(name="Posição", value=role.position, inline=True)
        embed.add_field(name="Mencionável", value="Sim" if role.mentionable else "Não", inline=True)
        embed.add_field(name="Gerenciável", value="Sim" if role.managed else "Não", inline=True)
        embed.add_field(name="Membros com este cargo", value=len(role.members), inline=True)
        embed.add_field(name="Cargo padrão", value="Sim" if role.is_default() else "Não", inline=True)
        embed.add_field(name="Cargo de integração", value="Sim" if role.is_integration() else "Não", inline=True)
        embed.add_field(name="Cargo de boost", value="Sim" if role.is_premium_subscriber() else "Não", inline=True)
        embed.add_field(name="Criado em", value=role.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        
        embed.set_footer(text=f"Solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)