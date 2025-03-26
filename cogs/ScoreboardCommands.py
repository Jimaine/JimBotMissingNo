import Service.JimBotService as JimBotService
import discord
from discord import app_commands
from discord.ext import commands
from Models.JimBotSecrets import JimBotSecrets


jim_bot_secrets = JimBotSecrets()

class ScoreboardCommands(commands.Cog):
    # initialize ScoreboardCommands
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Scoreboard commands ready')

    # static methods   
    @staticmethod
    def get_trainer_choices():
        trainer_choices = []
        
        for name, value in JimBotService.get_trainer_choices(is_only_active_trainers = True).items():
            trainer_choices.append(discord.app_commands.Choice(name=name, value=value))

        return trainer_choices

    @staticmethod
    def get_season_choices():
        season_choices = []
        
        for name, value in JimBotService.get_season_choices(is_only_active_season = False).items():
            season_choices.append(discord.app_commands.Choice(name=name, value=value))

        return season_choices  

    # app commands    
    @app_commands.command(name="punktetabelle_kampf", description="Fuege einen Pokemon-Kampf fuer die aktuelle Saison hinzu")
    @app_commands.describe(sieger='Gewinner des Kampfes', verlierer='Verlierer des Kampfes')
    async def punktetabelle_kampf(self, interaction: discord.Interaction, sieger: str, verlierer: str):
        service_result = await JimBotService.scoreboard_battle(sieger, verlierer, created_by = interaction.user.name)
        await interaction.response.send_message(str(service_result))

    @app_commands.command(name="punktetabelle_tausch", description="Fuege einen Karten-Tausch fuer die aktuelle Saison hinzu")
    @app_commands.describe(trainer_eins='Waehle den ersten Trainer vom Tausch', trainer_zwei='Waehle den zweiten Trainer vom Tausch')
    async def punktetabelle_tausch(self, interaction: discord.Interaction, trainer_eins: str, trainer_zwei: str):
        service_result = await JimBotService.scoreboard_trade(trainer_eins, trainer_zwei, created_by = interaction.user.name)
        await interaction.response.send_message(str(service_result))

    @app_commands.command(name="punktetabelle_anzeigen", description="Zeigt die Punktetabelle einer Saison an")
    @app_commands.describe(alle_saisons='Alle erfassten Saisons')
    async def punktetabelle_anzeigen(self, interaction: discord.Interaction, alle_saisons: str = None):
        service_result = await JimBotService.scoreboard_show(alle_saisons)   
        await interaction.response.send_message(str(service_result))

    # autocompletes
    @punktetabelle_kampf.autocomplete('sieger')
    @punktetabelle_kampf.autocomplete('verlierer')
    @punktetabelle_tausch.autocomplete('trainer_eins')
    @punktetabelle_tausch.autocomplete('trainer_zwei')
    async def trainers_autocomplete(self, interaction: discord.Interaction, current: str):
        trainer_choices = self.get_trainer_choices()
        return [app_commands.Choice(name=trainer_choice.name, value=trainer_choice.value) for trainer_choice in trainer_choices if current.lower() in trainer_choice.name.lower()]

    @punktetabelle_anzeigen.autocomplete('alle_saisons')
    async def seasons_autocomplete(self, interaction: discord.Interaction, current: str):
        season_choices = self.get_season_choices()
        return [app_commands.Choice(name=season_choice.name, value=season_choice.value) for season_choice in season_choices if current.lower() in season_choice.name.lower()]

        
async def setup(bot):
    await bot.add_cog(
        ScoreboardCommands(bot), 
        guilds=[
            discord.Object(id=jim_bot_secrets.discord_missing_no_guild_id),
            discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)
        ]
    )
