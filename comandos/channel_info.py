import discord
from datetime import datetime

def setup_channel_info(bot):
    @bot.command(name='channel_info', help='Mostra informações detalhadas sobre um canal de texto. Uso: A.channel_info <canal>')
    async def channel_info(ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        category = channel.category.name if channel.category else "Nenhuma"
        topic = channel.topic if channel.topic else "Nenhum"
        embed = discord.Embed(
            title=f"Informações do Canal: {channel.name}",
            description=f"Aqui estão as informações detalhadas sobre o canal {channel.mention}:",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"Servidor: {ctx.guild.name}", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.add_field(name="Nome", value=f"```{channel.name}```", inline=True)
        embed.add_field(name="ID", value=f"```{channel.id}```", inline=True)
        embed.add_field(name="Tipo", value=f"```{str(channel.type).title()}```", inline=True)
        embed.add_field(name="Categoria", value=f"```{category}```", inline=True)
        embed.add_field(name="Posição", value=f"```{channel.position}```", inline=True)
        embed.add_field(name="NSFW", value=f"```Sim```" if channel.is_nsfw() else "```Não```", inline=True)
        embed.add_field(name="Notícias", value=f"```Sim```" if channel.is_news() else "```Não```", inline=True)
        embed.add_field(name="Criado em", value=f"```{channel.created_at.strftime('%d/%m/%Y %H:%M:%S')}```", inline=True)
        embed.add_field(name="Tópico", value=f"```{topic}```", inline=False)
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @bot.tree.command(name='channel_info', description='Mostra informações detalhadas sobre um canal de texto.')
    async def channel_info(interaction: discord.Interaction, channel: discord.TextChannel = None):
        if channel is None:
            channel = interaction.channel

        category = channel.category.name if channel.category else "Nenhuma"
        topic = channel.topic if channel.topic else "Nenhum"
        
        embed = discord.Embed(
            title=f"Informações do Canal: {channel.name}",
            description=f"Aqui estão as informações detalhadas sobre o canal {channel.mention}:",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"Servidor: {interaction.guild.name}", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.add_field(name="Nome", value=f"```{channel.name}```", inline=True)
        embed.add_field(name="ID", value=f"```{channel.id}```", inline=True)
        embed.add_field(name="Tipo", value=f"```{str(channel.type).title()}```", inline=True)
        embed.add_field(name="Categoria", value=f"```{category}```", inline=True)
        embed.add_field(name="Posição", value=f"```{channel.position}```", inline=True)
        embed.add_field(name="NSFW", value=f"```Sim```" if channel.is_nsfw() else "```Não```", inline=True)
        embed.add_field(name="Notícias", value=f"```Sim```" if channel.is_news() else "```Não```", inline=True)
        embed.add_field(name="Criado em", value=f"```{channel.created_at.strftime('%d/%m/%Y %H:%M:%S')}```", inline=True)
        embed.add_field(name="Tópico", value=f"```{topic}```", inline=False)
        embed.set_footer(text=f"Solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)