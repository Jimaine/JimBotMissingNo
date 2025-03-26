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
        print('ScoreboardCommands cog loaded')

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
    @app_commands.command(name="scoreboard_battle", description="Add a battle to the scoreboard")
    @app_commands.describe(winner='Trainers who wins', looser='Trainers to choose from')
    async def scoreboard_battle(self, interaction: discord.Interaction, winner: str, looser: str):
        service_result = await JimBotService.scoreboard_battle(winner, looser, created_by = interaction.user.name)
        await interaction.response.send_message(str(service_result))

    @app_commands.command(name="scoreboard_trade", description="Add a trade to the scoreboard")
    @app_commands.describe(trainer_one='Trainers to choose from', trainer_two='Trainers to choose from')
    async def scoreboard_trade(self, interaction: discord.Interaction, trainer_one: str, trainer_two: str):
        service_result = await JimBotService.scoreboard_trade(trainer_one, trainer_two, created_by = interaction.user.name)
        await interaction.response.send_message(str(service_result))

    @app_commands.command(name="scoreboard_show", description="Shows the results of a season")
    @app_commands.describe(season='Seasons to choose from')
    async def scoreboard_show(self, interaction: discord.Interaction, season: str = None):
        scoreboard_results = await JimBotService.scoreboard_show(season)     
        await interaction.response.send_message(scoreboard_results)

    # autocompletes
    @scoreboard_battle.autocomplete('winner')
    @scoreboard_battle.autocomplete('looser')
    @scoreboard_trade.autocomplete('trainer_one')
    @scoreboard_trade.autocomplete('trainer_two')
    async def trainers_autocomplete(self, interaction: discord.Interaction, current: str):
        trainer_choices = self.get_trainer_choices()
        return [app_commands.Choice(name=trainer_choice.name, value=trainer_choice.value) for trainer_choice in trainer_choices if current.lower() in trainer_choice.name.lower()]

    @scoreboard_show.autocomplete('season')
    async def seasons_autocomplete(self, interaction: discord.Interaction, current: str):
        season_choices = self.get_season_choices()
        return [app_commands.Choice(name=season_choice.name, value=season_choice.value) for season_choice in season_choices if current.lower() in season_choice.name.lower()]

        
async def setup(bot):
    await bot.add_cog(ScoreboardCommands(bot), guilds=[discord.Object(id=jim_bot_secrets.discord_missing_no_guild_id),discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)])