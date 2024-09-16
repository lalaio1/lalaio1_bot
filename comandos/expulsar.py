import discord
from discord.ext import commands

def setup_expulsar(bot):
    @bot.command(name='expulsar', help='Expulsa um membro do servidor')
    @commands.has_permissions(kick_members=True)
    async def expulsar(ctx, membro: discord.Member, *, motivo=None):
        if not ctx.guild.me.guild_permissions.kick_members:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para expulsar membros neste servidor.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)
            return

        if membro == ctx.author:
            embed = discord.Embed(
                title='❌ Operação Inválida',
                description="Você não pode se expulsar.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)
            return

        if not ctx.guild.me.top_role > membro.top_role:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não posso expulsar membros com cargos superiores ao meu.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)
            return

        if not ctx.author.guild_permissions.kick_members:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Você não tem permissão para expulsar membros neste servidor.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)
            return

        try:
            await membro.kick(reason=motivo)
            embed = discord.Embed(
                title='✅ Membro Expulso',
                description=f"{membro.mention} foi expulso do servidor.",
                color=discord.Color.green()
            )
            embed.add_field(name="Motivo", value=motivo if motivo else "Não especificado", inline=False)
            embed.set_footer(text=f'Expulso por {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)

            dm_embed = discord.Embed(
                title='⚠️ Você foi Expulso',
                description=f'Você foi expulso do servidor **{ctx.guild.name}**.',
                color=discord.Color.red()
            )
            if motivo:
                dm_embed.add_field(name='📜 Motivo', value=motivo, inline=False)
            dm_embed.set_footer(text=f'Expulso por {ctx.author}', icon_url=ctx.author.avatar.url)
            await membro.send(embed=dm_embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para expulsar membros neste servidor.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title='❌ Erro ao Expulsar Membro',
                description=f"Ocorreu um erro ao tentar expulsar {membro.mention}: {e}",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro Desconhecido',
                description=f"Ocorreu um erro desconhecido ao tentar expulsar {membro.mention}: {e}",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await ctx.reply(embed=embed)

    @bot.tree.command(name='expulsar', description='Expulsa um membro do servidor')
    @discord.app_commands.describe(membro='O membro a ser expulso', motivo='O motivo da expulsão')
    async def expulsar_slash(interaction: discord.Interaction, membro: discord.Member, motivo: str = None):
        if not interaction.guild.me.guild_permissions.kick_members:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para expulsar membros neste servidor.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)
            return

        if membro == interaction.user:
            embed = discord.Embed(
                title='❌ Operação Inválida',
                description="Você não pode se expulsar.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)
            return

        if not interaction.guild.me.top_role > membro.top_role:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não posso expulsar membros com cargos superiores ao meu.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)
            return

        if not interaction.user.guild_permissions.kick_members:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Você não tem permissão para expulsar membros neste servidor.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)
            return

        try:
            await membro.kick(reason=motivo)
            embed = discord.Embed(
                title='✅ Membro Expulso',
                description=f"{membro.mention} foi expulso do servidor.",
                color=discord.Color.green()
            )
            embed.add_field(name="Motivo", value=motivo if motivo else "Não especificado", inline=False)
            embed.set_footer(text=f'Expulso por {interaction.user}', icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)

            dm_embed = discord.Embed(
                title='⚠️ Você foi Expulso',
                description=f'Você foi expulso do servidor **{interaction.guild.name}**.',
                color=discord.Color.red()
            )
            if motivo:
                dm_embed.add_field(name='📜 Motivo', value=motivo, inline=False)
            dm_embed.set_footer(text=f'Expulso por {interaction.user}', icon_url=interaction.user.avatar.url)
            await membro.send(embed=dm_embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title='❌ Permissão Insuficiente',
                description="Eu não tenho permissão para expulsar membros neste servidor.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title='❌ Erro ao Expulsar Membro',
                description=f"Ocorreu um erro ao tentar expulsar {membro.mention}: {e}",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='❌ Erro Desconhecido',
                description=f"Ocorreu um erro desconhecido ao tentar expulsar {membro.mention}: {e}",
                color=discord.Color.red()
            )
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")
            await interaction.response.send_message(embed=embed)
