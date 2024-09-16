import discord
import json


def setup_add_command(bot):
    @bot.command(name='add_command_sexo', help='Adiciona um novo comando à tabela de comandos do bot.')
    async def add_command(ctx, name: str, description: str, syntax: str, *examples: str):
        try:
            with open('./commands/commands.json', 'r', encoding='utf-8') as file:
                commands_list = json.load(file)

            for command in commands_list:
                if command['name'] == name:
                    await ctx.reply(f"ℹ️ O comando '{name}' já existe na tabela.")
                    return

            new_command = {
                'name': name,
                'description': description,
                'syntax': syntax,
                'examples': list(examples)
            }
            commands_list.append(new_command)

            with open('./commands/commands.json', 'w', encoding='utf-8') as file:
                json.dump(commands_list, file, indent=4, ensure_ascii=False)

            embed = discord.Embed(
                title="🛠️ Novo Comando Adicionado",
                description=f"O comando `{name}` foi adicionado à tabela de comandos com sucesso!",
                color=discord.Color.green()
            )
            embed.add_field(name="Descrição", value=description, inline=False)
            embed.add_field(name="Sintaxe", value=syntax, inline=False)
            if examples:
                embed.add_field(name="Exemplos", value='\n'.join(examples), inline=False)
            embed.set_footer(text="Lalaio Bot", icon_url="https://i.ibb.co/WDfBJ2g/lalaio1.png")

            await ctx.reply(embed=embed)

        except Exception as e:
            await ctx.reply(f"🚫 Ocorreu um erro ao adicionar o comando: {str(e)}")