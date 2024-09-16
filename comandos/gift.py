import discord
import random
import asyncio
import os
import uuid

services = {
    "amazon": {"format": "xxxx-xxxx-xxxx", "rolls": [4, 4, 4]},
    "roblox": {"format": "xxx-xxx-xxxx", "rolls": [3, 3, 4]},
    "webkinz": {"format": "xxxxxxxx", "rolls": [8]},
    "fortnite": {"format": "xxxxx-xxxx-xxxx", "rolls": [5, 4, 4]},
    "imvu": {"format": "xxxxxxxxxx", "rolls": [10]},
    "ebay": {"format": "xxxxxxxxxx", "rolls": [10]},
    "netflix": {"format": "xxxx-xxxx-xxxx", "rolls": [4, 4, 4]},
    "itunes": {"format": "xxxxxxxxxxxxxxxx", "rolls": [16]},
    "paypal": {"format": "xxxx-xxxx-xxxx", "rolls": [4, 4, 4]},
    "visa": {"format": "xxxx-xxxx-xxxx-xxxx", "rolls": [4, 4, 4, 4]},
    "pokemontgc": {"format": "xxx-xxxx-xxx-xxx", "rolls": [3, 4, 3, 3]},
    "playstation": {"format": "xxxx-xxxx-xxxx", "rolls": [4, 4, 4]},
    "steam": {"format": "xxxx-xxxx-xxxx", "rolls": [4, 4, 4]},
    "xbox": {"format": "xxxxx-xxxxx-xxxxx-xxxxx-xxxxx", "rolls": [5, 5, 5, 5, 5]},
    "playstore": {"format": "xxxx-xxxx-xxxx-xxxx-xxxx", "rolls": [4, 4, 4, 4, 4]},
    "minecraft": {"format": "xxxx-xxxx-xxxx", "rolls": [4, 4, 4]}
}

def setup_gift(bot):
    @bot.command()
    async def gift(ctx, service):
        service = service.lower()

        if service not in services:
            available_services = ', '.join(services.keys())
            embed = discord.Embed(
                title="Serviços Disponíveis",
                description=f"Escolha entre: {available_services}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
            return

        await ctx.reply(f"```Fix\nGerando códigos para {service} ⏳```")
        
        await asyncio.create_task(generate_codes(ctx, service))

async def generate_codes(ctx, service):
    count = 50000

    result = ""
    for _ in range(count):
        format_str = services[service]["format"]

        generated_code = generate_code(format_str)
        result += generated_code + "\n"

    unique_filename = f"{service}_codes_{uuid.uuid4()}.txt"

    with open(unique_filename, "w") as file:
        file.write(result)

    embed = discord.Embed(
        title=f"Códigos Gerados para {service}",
        description=f"Foram gerados {count} códigos para {service}.",
        color=discord.Color.green()
    )
    await ctx.reply(embed=embed, file=discord.File(unique_filename, filename=unique_filename))

    os.remove(unique_filename)

def generate_code(format_str):
    data = "qwertyuioplkjhgfdsazxcvbnm1234567890QWERTYUIOPLKJHGFDSAZXCVBNM"
    code = ""

    for char in format_str:
        if char == "x":
            code += random.choice(data)
        else:
            code += char

    return code