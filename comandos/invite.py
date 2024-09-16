import discord

def setup_invite(bot):
    @bot.command(name='invite', help='Gera um convite personalizado para o servidor específico')
    async def generate_invite(ctx):
        try:
            bot_invite_url = "https://discord.com/oauth2/authorize?client_id=1215660441909465088&permissions=8&integration_type=0&scope=bot"

            invite = await ctx.channel.create_invite(max_uses=0, max_age=0, unique=True)

            embed = discord.Embed(
                title="Convite Personalizado",
                description=f"Olá {ctx.author.mention}, aqui está o seu convite personalizado para este servidor!",
                color=discord.Color.blurple()
            )
            embed.add_field(name="Link do Convite:", value=invite.url)
            embed.add_field(name="Adicione o Bot ao seu Servidor", value=bot_invite_url, inline=False)

            await ctx.reply(embed=embed)

        except discord.Forbidden:
            error_embed = discord.Embed(
                title="Erro ao Gerar Convite",
                description="Não tenho permissão para criar convites neste canal.",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Erro ao Gerar Convite",
                description=f"Ocorreu um erro ao tentar gerar o convite: {e}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=error_embed)