import discord
import requests
from discord.ui import Button, View

class TokenInfoView(View):
    def __init__(self, full_info):
        super().__init__()
        self.full_info = full_info

    @discord.ui.button(label="Baixar Informações Completas 🔎", style=discord.ButtonStyle.blurple)
    async def download_button_callback(self, interaction: discord.Interaction, button: Button):
        with open("token_info.txt", "w", encoding='utf-8') as file:
            file.write(self.full_info)
        
        await interaction.response.send_message(file=discord.File("token_info.txt"), ephemeral=True)

def setup_tokeninfo(bot):
    @bot.command(name='tokeninfo', help='Obtém informações detalhadas sobre um token Discord')
    async def tokeninfo(ctx, token):
        try:
            await ctx.reply("```Fix\nRecuperando informações ⏳\n```")

            user_response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()

            if 'username' in user_response and 'discriminator' in user_response and 'id' in user_response and 'avatar' in user_response:
                username_discord = f"{user_response['username']}#{user_response['discriminator']}"
                user_id_discord = user_response['id']
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_id_discord}/{user_response['avatar']}.png"
            else:
                await ctx.reply("```😐 Token inválido ou resposta inesperada da API.```")
                return

            email_discord = user_response.get('email', 'N/A')
            phone_discord = user_response.get('phone', 'N/A')
            mfa_discord = user_response.get('mfa_enabled', False)

            nitro_response = requests.get('https://discord.com/api/v8/users/@me/billing/subscriptions', headers={'Authorization': token}).json()
            nitro_discord = 'Nitro' if nitro_response else 'Nenhum'

            billing_response = requests.get('https://discord.com/api/v8/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
            if billing_response:
                payment_methods = [':credit_card:' if method['type'] == 1 else ':paypal:' for method in billing_response]
                payment_methods_str = ' '.join(payment_methods)
            else:
                payment_methods_str = 'Nenhum'

            guilds_response = requests.get('https://discord.com/api/v8/users/@me/guilds', headers={'Authorization': token}).json()
            guilds_info = [f"{guild['name']} ({guild['id']})" for guild in guilds_response]
            guilds_info_str = '\n'.join(guilds_info) if guilds_info else 'Nenhum'

            friends_response = requests.get('https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': token}).json()
            friends_info = [f"{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})" for friend in friends_response]
            friends_info_str = '\n'.join(friends_info) if friends_info else 'Nenhum'

            embed = discord.Embed(title="Informações do Token Discord", color=discord.Color.red())
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name="Nome de Usuário", value=f"```\n{username_discord}\n```", inline=False)
            embed.add_field(name="ID", value=f"```\n{user_id_discord}\n```", inline=False)
            embed.add_field(name="E-mail", value=f"```\n{email_discord}\n```", inline=False)
            embed.add_field(name="Telefone", value=f"```\n{phone_discord}\n```", inline=False)
            embed.add_field(name="Nitro", value=f"```\n{nitro_discord}\n```", inline=False)
            embed.add_field(name="Autenticação Multifator", value=f"```\n{mfa_discord}\n```", inline=False)

            full_info = f"""
==========================================
Informações do Token Discord
==========================================

Nome de Usuário:         
{username_discord}

ID:                      
{user_id_discord}

E-mail:                  
{email_discord}

Telefone:                
{phone_discord}

Token:                   
{token}

Nitro:                   
{nitro_discord}

Autenticação Multifator: 
{mfa_discord}
            


==========================================
Métodos de Pagamento
==========================================
        
{payment_methods_str}
        
==========================================
Servidores
==========================================
        
{guilds_info_str}
        
==========================================
Amigos
==========================================
        
{friends_info_str}
            """
            view = TokenInfoView(full_info)
            await ctx.reply(embed=embed, view=view)

        except Exception as e:
            print(e)
            await ctx.reply("```🙁 Não foi possível recuperar informações com este token.```")


    @bot.tree.command(name='tokeninfo', description='Obtém informações detalhadas sobre um token de usuario do Discord')
    async def tokeninfo(interaction: discord.Interaction, token: str):
        try:
            user_response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()

            if 'username' in user_response and 'discriminator' in user_response and 'id' in user_response and 'avatar' in user_response:
                username_discord = f"{user_response['username']}#{user_response['discriminator']}"
                user_id_discord = user_response['id']
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_id_discord}/{user_response['avatar']}.png"
            else:
                await interaction.response.send_message("```😐 Token inválido ou resposta inesperada da API.```", ephemeral=True)
                return

            email_discord = user_response.get('email', 'N/A')
            phone_discord = user_response.get('phone', 'N/A')
            mfa_discord = user_response.get('mfa_enabled', False)

            nitro_response = requests.get('https://discord.com/api/v8/users/@me/billing/subscriptions', headers={'Authorization': token}).json()
            nitro_discord = 'Nitro' if nitro_response else 'Nenhum'

            billing_response = requests.get('https://discord.com/api/v8/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
            if billing_response:
                payment_methods = [':credit_card:' if method['type'] == 1 else ':paypal:' for method in billing_response]
                payment_methods_str = ' '.join(payment_methods)
            else:
                payment_methods_str = 'Nenhum'

            guilds_response = requests.get('https://discord.com/api/v8/users/@me/guilds', headers={'Authorization': token}).json()
            guilds_info = [f"{guild['name']} ({guild['id']})" for guild in guilds_response]
            guilds_info_str = '\n'.join(guilds_info) if guilds_info else 'Nenhum'

            friends_response = requests.get('https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': token}).json()
            friends_info = [f"{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})" for friend in friends_response]
            friends_info_str = '\n'.join(friends_info) if friends_info else 'Nenhum'

            embed = discord.Embed(title="Informações do Token Discord", color=discord.Color.red())
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name="Nome de Usuário", value=f"```\n{username_discord}\n```", inline=False)
            embed.add_field(name="ID", value=f"```\n{user_id_discord}\n```", inline=False)
            embed.add_field(name="E-mail", value=f"```\n{email_discord}\n```", inline=False)
            embed.add_field(name="Telefone", value=f"```\n{phone_discord}\n```", inline=False)
            embed.add_field(name="Nitro", value=f"```\n{nitro_discord}\n```", inline=False)
            embed.add_field(name="Autenticação Multifator", value=f"```\n{mfa_discord}\n```", inline=False)

            full_info = f"""
==========================================
Informações do Token Discord
==========================================

Nome de Usuário:         
{username_discord}

ID:                      
{user_id_discord}

E-mail:                  
{email_discord}

Telefone:                
{phone_discord}

Token:                   
{token}

Nitro:                   
{nitro_discord}

Autenticação Multifator: 
{mfa_discord}
            


==========================================
Métodos de Pagamento
==========================================
        
{payment_methods_str}
        
==========================================
Servidores
==========================================
        
{guilds_info_str}
        
==========================================
Amigos
==========================================
        
{friends_info_str}
            """
            view = TokenInfoView(full_info)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        except Exception as e:
            print(e)
            await interaction.response.send_message("```🙁 Não foi possível recuperar informações com este token.```", ephemeral=True)