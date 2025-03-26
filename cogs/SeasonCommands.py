import Service.JimBotService as JimBotService
import discord
from discord import app_commands
from discord.ext import commands
from Models.JimBotSecrets import JimBotSecrets


jim_bot_secrets = JimBotSecrets()

class SeasonCommands(commands.Cog):
    # initialize SeasonCommands
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Season commands ready')

    # static methods    
    @staticmethod
    def get_season_choices():
        season_choices = []
        
        for name, value in JimBotService.get_season_choices(is_only_active_season = False).items():
            season_choices.append(discord.app_commands.Choice(name=name, value=value))

        return season_choices

    # app commands
    @app_commands.command(name="saison_hinzufuegen", description="Fuege eine neue Saison hinzu")
    @app_commands.describe(name='Der Name der neuen Saison', punkte_fuer_orden='Die Anzahl an Punkten, die für den Orden benoetigt werden')
    async def saison_hinzufuegen(self, interaction: discord.Interaction, name: str, punkte_fuer_orden: int):
        service_result = await JimBotService.season_add(name, punkte_fuer_orden, created_by = interaction.user.name)
        await interaction.response.send_message(str(service_result))

    @app_commands.command(name="saison_aktivieren", description="Aktiviere eine Saison")
    @app_commands.describe(alle_saisons='Alle erfassten Saisons')
    async def saison_aktivieren(self, interaction: discord.Interaction, alle_saisons: str):
        service_result = await JimBotService.season_activate(alle_saisons)
        await interaction.response.send_message(str(service_result))

    # autocompletes
    @saison_aktivieren.autocomplete('alle_saisons')
    async def seasons_autocomplete(self, interaction: discord.Interaction, current: str):
        season_choices = self.get_season_choices()
        return [app_commands.Choice(name=season_choice.name, value=season_choice.value) for season_choice in season_choices if current.lower() in season_choice.name.lower()]

        
async def setup(bot):
    await bot.add_cog(
        SeasonCommands(bot), 
        guilds=[
            discord.Object(id=jim_bot_secrets.discord_missing_no_guild_id),
            discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)
        ]
    )
