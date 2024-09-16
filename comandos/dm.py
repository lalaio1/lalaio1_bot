import discord

def setup_dm(bot):
    @bot.command(name='dm', help='Envia uma mensagem direta para um membro específico')
    async def dm(ctx, member: discord.Member, *, message: str):
        if member.bot:
            embed = discord.Embed(
                title='Erro',
                description="Não é possível enviar mensagens diretas para bots.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.send(message)
            embed = discord.Embed(
                title='Mensagem Enviada',
                description=f"Mensagem enviada para {member.mention}.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title='Erro',
                description=f"❌ Não foi possível enviar a mensagem para {member.mention}. O usuário pode ter desabilitado as mensagens diretas.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Erro ao enviar mensagem para {member.name}: {e}")
            embed = discord.Embed(
                title='Erro',
                description=f"❌ Ocorreu um erro ao enviar a mensagem para {member.mention}. Por favor, tente novamente mais tarde.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

