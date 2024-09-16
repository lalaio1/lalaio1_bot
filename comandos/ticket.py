import discord
from discord.ext import commands
import json
import os

os.makedirs('json/ticket', exist_ok=True)

def setup_ticket(bot):

    def load_ticket_config():
        try:
            with open('json/ticket/config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_ticket_config(config):
        with open('json/ticket/config.json', 'w') as f:
            json.dump(config, f, indent=4)

    def load_ticket_data():
        try:
            with open('json/ticket/tickets.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_ticket_data(data):
        with open('json/ticket/tickets.json', 'w') as f:
            json.dump(data, f, indent=4)

    ticket_config = load_ticket_config()

    class TicketForm(discord.ui.Modal, title="Configurar Tickets"):
        server_id = discord.ui.TextInput(label="ID do Servidor", placeholder="Insira o ID do servidor", required=True)
        role_id = discord.ui.TextInput(label="ID do Cargo Atendente", placeholder="Insira o ID do cargo atendente", required=True)
        channel_id = discord.ui.TextInput(label="ID do Canal de Logs", placeholder="Insira o ID do canal de logs", required=True)
        ticket_name = discord.ui.TextInput(label="Nome do Ticket", placeholder="Insira o nome do ticket", required=True)
        ticket_description = discord.ui.TextInput(label="Descrição do Ticket", placeholder="Insira a descrição do ticket", style=discord.TextStyle.paragraph, required=True)

        async def on_submit(self, interaction: discord.Interaction):
            ticket_config['server_id'] = int(self.server_id.value)
            ticket_config['role_id'] = int(self.role_id.value)
            ticket_config['channel_id'] = int(self.channel_id.value)
            ticket_config['ticket_name'] = self.ticket_name.value
            ticket_config['ticket_description'] = self.ticket_description.value
            
            save_ticket_config(ticket_config)
            
            embed = discord.Embed(
                title=self.ticket_name.value,
                description=self.ticket_description.value,
                color=0x8A2BE2
            )
            
            await interaction.response.send_message(embed=embed, view=DropdownView())

    class Dropdown(discord.ui.Select):
        def __init__(self):
            options = [
                discord.SelectOption(value="atendimento", label="Atendimento", emoji="📩"),
                discord.SelectOption(value="reporte", label="Reporte de Bugs", emoji="🐛"),
                discord.SelectOption(value="denuncia", label="Denúncia", emoji="🚨"),
                discord.SelectOption(value="duvidas", label="Dúvidas", emoji="❓")
            ]
            super().__init__(
                placeholder="Selecione uma opção...",
                min_values=1,
                max_values=1,
                options=options,
                custom_id="persistent_view:dropdown_main"
            )
        
        async def callback(self, interaction: discord.Interaction):
            try:
                if self.values[0] == "atendimento":
                    await interaction.response.send_message("Clique abaixo para criar um ticket", ephemeral=True, view=CreateTicket("Atendimento"))
                elif self.values[0] == "reporte":
                    message = (
                        "🐛 **Reporte de Bugs** 🐛\n\n"
                        "Para reportar um Bug do Servidor, atente-se às instruções:\n\n"
                        "Envie o máximo de detalhes sobre o bug (incluindo descrição e fotos).\n\n"
                        "Com essas informações em mãos, crie um ticket abaixo e envie o seu reporte. Clique no botão abaixo para criar um atendimento."
                    )
                    await interaction.response.send_message(message, ephemeral=True, view=CreateTicket("Reporte de Bugs"))
                elif self.values[0] == "denuncia":
                    message = (
                        "🚨 **Denúncia** 🚨\n\n"
                        "Para fazer uma denúncia, precisamos do motivo da denúncia, dos autores do ocorrido e das provas.\n\n"
                        "Não crie um ticket de denúncia apenas para testar a ferramenta ou para tirar dúvidas (existem outros espaços para isso!).\n\n"
                        "Se desejar prosseguir com sua denúncia, crie um atendimento abaixo."
                    )
                    await interaction.response.send_message(message, ephemeral=True, view=CreateTicket("Denúncia"))
                elif self.values[0] == "duvidas":
                    message = (
                        "❓ **Dúvidas** ❓\n\n"
                        "Para esclarecer dúvidas, por favor, crie um ticket abaixo. Nossa equipe está pronta para ajudar com qualquer questão que você possa ter."
                    )
                    await interaction.response.send_message(message, ephemeral=True, view=CreateTicket("Dúvidas"))
            except Exception as e:
                await interaction.response.send_message(f"Erro ao processar sua solicitação: {str(e)}", ephemeral=True)

    class DropdownView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.add_item(Dropdown())

    class TicketButtons(discord.ui.View):
        def __init__(self, interaction):
            super().__init__(timeout=None)
            self.interaction = interaction

        @discord.ui.button(label="Fechar Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id="ticket_buttons:close")
        async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
            try:
                mod_role = interaction.guild.get_role(ticket_config['role_id'])
                if mod_role in interaction.user.roles:
                    transcript_file_path = await save_ticket_transcript(interaction.channel)
                    
                    creator_id = None
                    with open('json/ticket/ticket.json', 'r') as f:
                        ticket_data = json.load(f)
                    creator_id = ticket_data.get('creator')

                    creator_member = interaction.guild.get_member(int(creator_id)) if creator_id else None
                    if creator_member:
                        await creator_member.send(file=discord.File(transcript_file_path, "transcript.json"))
                    
                    log_channel = interaction.guild.get_channel(ticket_config['channel_id'])
                    if log_channel:
                        await log_channel.send(file=discord.File(transcript_file_path, "transcript.json"))
                    
                    os.remove(transcript_file_path)
                    await interaction.channel.delete()
                else:
                    await interaction.response.send_message("Você não tem permissão para fechar este ticket.", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"Erro ao processar sua solicitação: {str(e)}", ephemeral=True)

    class CreateTicket(discord.ui.View):
        def __init__(self, ticket_type):
            super().__init__(timeout=300)
            self.ticket_type = ticket_type

        @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.blurple, emoji="🆗", custom_id="create_ticket:open")
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            try:
                ticket_name = f"{interaction.user.name} - {interaction.user.id}"
                ticket = None

                for thread in interaction.channel.threads:
                    if f"{interaction.user.id}" in thread.name:
                        if thread.archived:
                            ticket = thread
                        else:
                            await interaction.response.send_message(ephemeral=True, content="Você já tem um atendimento em andamento!")
                            return

                async for thread in interaction.channel.archived_threads(private=True):
                    if f"{interaction.user.id}" in thread.name:
                        if thread.archived:
                            ticket = thread
                        else:
                            await interaction.response.send_message(content="Você já tem um atendimento em andamento!", ephemeral=True)
                            return

                if ticket is not None:
                    await ticket.edit(archived=False, locked=False)
                    await ticket.edit(name=ticket_name, auto_archive_duration=10080, invitable=False)
                else:
                    ticket = await interaction.channel.create_thread(name=f"{self.ticket_type} - {ticket_name}", auto_archive_duration=10080)
                    await ticket.edit(invitable=False)

                mod_role = interaction.guild.get_role(ticket_config['role_id'])
                await interaction.response.send_message(ephemeral=True, content=f"Criei um ticket para você! {ticket.mention}")
                await ticket.send(f"📩  **|** {interaction.user.mention} criou um ticket para **{self.ticket_type}**!\n\n{mod_role.mention}, por favor, responda ao ticket.", view=TicketButtons(interaction))
                
                with open('json/ticket/ticket.json', 'w') as f:
                    json.dump({"name": ticket_name, "id": ticket.id, "creator": str(interaction.user.id)}, f, indent=4)
                    
            except Exception as e:
                await interaction.response.send_message(f"Erro ao processar sua solicitação: {str(e)}", ephemeral=True)

    async def save_ticket_transcript(channel):
        try:
            messages = []
            async for message in channel.history(limit=1000):
                messages.append({
                    "author": str(message.author),
                    "content": message.content,
                    "timestamp": message.created_at.isoformat()
                })
            transcript = {"messages": messages}
            transcript_file_path = 'transcript.json'
            with open(transcript_file_path, 'w') as file:
                json.dump(transcript, file, indent=4)
            return transcript_file_path
        except Exception as e:
            print(f"Erro ao salvar transcrição: {str(e)}")
            return io.StringIO("Erro ao salvar transcrição.")

    @bot.tree.command(name='setupticket', description='Configura o ticket no servidor')
    async def setupticket(interaction: discord.Interaction):
        try:
            guild_id = str(interaction.guild.id)
            config_data = load_ticket_config()
            if guild_id in config_data:
                channel_id = config_data[guild_id]['channel_id']
                channel = bot.get_channel(channel_id)
                if channel:
                    embed = discord.Embed(
                        title=config_data[guild_id]['ticket_name'],
                        description=config_data[guild_id]['ticket_description'],
                        color=0x8A2BE2
                    )
                    message = await channel.send(embed=embed, view=DropdownView())
                    save_ticket_data({guild_id: {
                        str(message.id): {
                            'server_id': guild_id,
                            'role_id': config_data[guild_id]['role_id'],
                            'channel_id': channel_id,
                            'ticket_name': config_data[guild_id]['ticket_name'],
                            'ticket_description': config_data[guild_id]['ticket_description'],
                            'message_id': message.id
                        }
                    }})
                    await interaction.response.send_message("Ticket configurado com sucesso!", ephemeral=True)
                else:
                    await interaction.response.send_message("Canal não encontrado.", ephemeral=True)
            else:
                await interaction.response.send_message("Configuração não encontrada para este servidor.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erro ao configurar o ticket: {str(e)}", ephemeral=True)

    @bot.tree.command(name='deletarticket', description='Exclui um ticket e remove as informações do sistema')
    @commands.has_permissions(manage_guild=True)
    async def deletarticket(interaction: discord.Interaction, message_id: int):
        try:
            guild_id = str(interaction.guild.id)
            ticket_data = load_ticket_data()
            if guild_id in ticket_data and str(message_id) in ticket_data[guild_id]:
                channel = bot.get_channel(ticket_data[guild_id][str(message_id)]['channel_id'])
                message = await channel.fetch_message(message_id)
                await message.delete()
                del ticket_data[guild_id][str(message_id)]
                save_ticket_data(ticket_data)
                await interaction.response.send_message(f"Ticket excluído com sucesso!", ephemeral=True)
            else:
                await interaction.response.send_message(f"Ticket não encontrado.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erro ao excluir o ticket: {str(e)}", ephemeral=True)

    @bot.tree.command(name='configurartickets', description='Configura a central de tickets')
    async def configurartickets(interaction: discord.Interaction):
        try:
            modal = TicketForm()
            await interaction.response.send_modal(modal)
        except Exception as e:
            await interaction.response.send_message(f"Erro ao configurar a central de atendimento: {str(e)}", ephemeral=True)

