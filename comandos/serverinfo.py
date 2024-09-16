import discord # type: ignore
from discord.ext import commands # type: ignore
from datetime import datetime

def setup_serverinfo(bot):
    @bot.command(name='serverinfo', help='Mostra informações detalhadas sobre o servidor')
    async def serverinfo(ctx):
        guild = ctx.guild

        online_members = sum(member.status != discord.Status.offline for member in guild.members)
        offline_members = len(guild.members) - online_members
        bot_count = sum(1 for member in guild.members if member.bot)

        embed = discord.Embed(title=f"Informações do Servidor: {guild.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url)

        if guild.banner:
            embed.set_image(url=guild.banner.url)

        embed.add_field(name="🏰 Nome", value=f"```{guild.name}```", inline=True)
        embed.add_field(name="🆔 ID", value=f"```{guild.id}```", inline=True)
        embed.add_field(name="👑 Dono", value=f"```{guild.owner}```", inline=True)
        embed.add_field(name="👥 Total de Membros", value=f"```{guild.member_count}```", inline=True)
        embed.add_field(name="👤 Membros Humanos", value=f"```{guild.member_count - bot_count}```", inline=True)
        embed.add_field(name="🤖 Bots", value=f"```{bot_count}```", inline=True)
        embed.add_field(name="🟢 Membros Online", value=f"```{online_members}```", inline=True)
        embed.add_field(name="⚪ Membros Offline", value=f"```{offline_members}```", inline=True)
        embed.add_field(name="📚 Canais de Texto", value=f"```{len(guild.text_channels)}```", inline=True)
        embed.add_field(name="🔊 Canais de Voz", value=f"```{len(guild.voice_channels)}```", inline=True)
        embed.add_field(name="📜 Categorias", value=f"```{len(guild.categories)}```", inline=True)
        embed.add_field(name="🛡️ Cargos", value=f"```{len(guild.roles)}```", inline=True)
        embed.add_field(name="😃 Boosters", value=f"```{guild.premium_subscription_count}```", inline=True)
        embed.add_field(name="🎨 Emojis", value=f"```{len(guild.emojis)}```", inline=True)
        embed.add_field(name="📅 Criado em", value=f"```{guild.created_at.strftime('%d/%m/%Y')}```", inline=False)

        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        embed.timestamp = ctx.message.created_at

        await ctx.reply(embed=embed)

    @bot.tree.command(name='serverinfo', description='Mostra informações detalhadas sobre o servidor')
    async def serverinfo_tree(interaction: discord.Interaction):
        guild = interaction.guild

        online_members = sum(member.status != discord.Status.offline for member in guild.members)
        offline_members = len(guild.members) - online_members
        bot_count = sum(1 for member in guild.members if member.bot)

        embed = discord.Embed(
            title=f"Informações do Servidor: {guild.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=guild.icon.url)

        if guild.banner:
            embed.set_image(url=guild.banner.url)

        embed.add_field(name="🏰 Nome", value=f"```{guild.name}```", inline=True)
        embed.add_field(name="🆔 ID", value=f"```{guild.id}```", inline=True)
        embed.add_field(name="👑 Dono", value=f"```{guild.owner}```", inline=True)
        embed.add_field(name="👥 Total de Membros", value=f"```{guild.member_count}```", inline=True)
        embed.add_field(name="👤 Membros Humanos", value=f"```{guild.member_count - bot_count}```", inline=True)
        embed.add_field(name="🤖 Bots", value=f"```{bot_count}```", inline=True)
        embed.add_field(name="🟢 Membros Online", value=f"```{online_members}```", inline=True)
        embed.add_field(name="⚪ Membros Offline", value=f"```{offline_members}```", inline=True)
        embed.add_field(name="📚 Canais de Texto", value=f"```{len(guild.text_channels)}```", inline=True)
        embed.add_field(name="🔊 Canais de Voz", value=f"```{len(guild.voice_channels)}```", inline=True)
        embed.add_field(name="📜 Categorias", value=f"```{len(guild.categories)}```", inline=True)
        embed.add_field(name="🛡️ Cargos", value=f"```{len(guild.roles)}```", inline=True)
        embed.add_field(name="😃 Boosters", value=f"```{guild.premium_subscription_count}```", inline=True)
        embed.add_field(name="🎨 Emojis", value=f"```{len(guild.emojis)}```", inline=True)
        embed.add_field(name="📅 Criado em", value=f"```{guild.created_at.strftime('%d/%m/%Y')}```", inline=False)

        embed.set_footer(text=f"Solicitado por {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        embed.timestamp = datetime.utcnow()  # Use the current UTC time

        await interaction.response.send_message(embed=embed)