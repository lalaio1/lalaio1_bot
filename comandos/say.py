import discord
from discord.ext import commands

# Função para verificar se o autor é administrador
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

# Configuração dos comandos com mensagens de erro em embed
def setup_say(bot):
    @bot.command(name='say', help='Envia uma mensagem no canal onde o comando foi executado.')
    @is_admin()  # Apenas administradores podem usar este comando
    async def say(ctx, *, message: str):
        await ctx.message.delete()
        await ctx.send(message)

    @say.error
    async def say_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Erro: Argumentos Faltando",
                                  description="Uso correto: `L.say <mensagem>`",
                                  color=discord.Color.red())
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Erro: Permissão Negada",
                                  description="Somente administradores podem usar este comando.",
                                  color=discord.Color.red())
        else:
            embed = discord.Embed(title="Erro",
                                  description=f"Ocorreu um erro ao executar o comando `{ctx.command}`.",
                                  color=discord.Color.red())
        
        await ctx.send(embed=embed)

    @bot.command(name='sayhere', help='Envia uma mensagem no canal mencionado. Uso: A sayhere #canal <mensagem>')
    @is_admin()  # Apenas administradores podem usar este comando
    async def sayhere(ctx, channel: discord.TextChannel, *, message: str):
        await ctx.message.delete()
        await channel.send(message)

    @sayhere.error
    async def sayhere_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Erro: Argumentos Faltando",
                                  description="Uso correto: `A sayhere #canal <mensagem>`",
                                  color=discord.Color.red())
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Erro: Permissão Negada",
                                  description="Somente administradores podem usar este comando.",
                                  color=discord.Color.red())
        else:
            embed = discord.Embed(title="Erro",
                                  description=f"Ocorreu um erro ao executar o comando `{ctx.command}`.",
                                  color=discord.Color.red())
        
        await ctx.send(embed=embed)


    @bot.tree.command(name='say', description='Envia uma mensagem no canal onde o comando foi executado.')
    @is_admin()  # Apenas administradores podem usar este comando
    async def say(interaction: discord.Interaction, message: str):
        try:
            await interaction.response.send_message(message)
        except Exception as e:
            embed = discord.Embed(
                title="Erro",
                description=f"Ocorreu um erro ao executar o comando `say`: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name='sayhere', description='Envia uma mensagem no canal mencionado. Uso: /sayhere #canal <mensagem>')
    @is_admin()  # Apenas administradores podem usar este comando
    async def sayhere(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        try:
            await channel.send(message)
            await interaction.response.send_message("Mensagem enviada com sucesso!")
        except Exception as e:
            embed = discord.Embed(
                title="Erro",
                description=f"Ocorreu um erro ao executar o comando `sayhere`: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
