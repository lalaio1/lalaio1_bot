import requests
import discord
from discord.ext import commands

def setup_delete_webhook(bot):
    @bot.command(name='delete_webhook', help='Deleta uma webhook através da sua URL.')
    async def delete_webhook(ctx, webhook_url):
        try:
            response = requests.delete(webhook_url)

            if response.status_code == 204:
                embed = discord.Embed(
                    title='Webhook Deletada',
                    description='🎯 Webhook deletada com sucesso.',
                    color=discord.Color.green()
                )
                await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(
                    title='Erro ao Deletar Webhook',
                    description=f'😖 Erro ao deletar webhook. Status Code: {response.status_code}',
                    color=discord.Color.red()
                )
                await ctx.reply(embed=embed)

        except requests.exceptions.RequestException as e:
            embed = discord.Embed(
                title='Erro de Requisição',
                description=f'😫 Erro ao acessar a URL da webhook: {e}',
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='Erro Inesperado',
                description=f'😟 Ocorreu um erro inesperado: {e}',
                color=discord.Color.red()
            )
            await ctx.reply(embed=embed)


    @bot.tree.command(name='delete_webhook', description='Deleta uma webhook através da sua URL.')
    @discord.app_commands.describe(webhook_url='A URL da webhook a ser deletada')
    async def delete_webhook(interaction: discord.Interaction, webhook_url: str):
        try:
            response = requests.delete(webhook_url)

            if response.status_code == 204:
                embed = discord.Embed(
                    title='Webhook Deletada',
                    description='🎯 Webhook deletada com sucesso.',
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title='Erro ao Deletar Webhook',
                    description=f'😖 Erro ao deletar webhook. Status Code: {response.status_code}',
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed)

        except requests.exceptions.RequestException as e:
            embed = discord.Embed(
                title='Erro de Requisição',
                description=f'😫 Erro ao acessar a URL da webhook: {e}',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title='Erro Inesperado',
                description=f'😟 Ocorreu um erro inesperado: {e}',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)