import Service.JimBotService as JimBotService
import discord
from discord import app_commands
from discord.ext import commands
from Models.JimBotSecrets import JimBotSecrets


jim_bot_secrets = JimBotSecrets()

class Scoreboard(commands.Cog):
    # initialize scoreboard
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Scoreboard cog loaded')

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
 
    # commands
    @commands.command()
    async def sync_scoreboard(self, context) -> None:
        try:
            fmt = await context.bot.tree.sync(guild=context.guild)
            await context.send(
                f"Synced {len(fmt)} scoreboard commands to the current guild"
            )
        except Exception as exception:
            await context.send(
                f"Exception while syncing {exception}"
            )
        return      

    # app commands    
    @app_commands.command(name="scoreboard_battle", description="Add a battle to the scoreboard")
    @app_commands.describe(winner='Trainers who wins', looser='Trainers to choose from', season='Seasons to choose from')
    async def scoreboard_battle(self, interaction: discord.Interaction, winner: str, looser: str, season: str = None):
        is_updated = await JimBotService.scoreboard_battle(winner, looser, season)
        
        if is_updated:
            seasonName = "active season" if season is None else season
            await interaction.response.send_message(f"Scoreboard added 20 Points to {winner} as the winner and 10 Points to the opponent {looser} for the {seasonName} succesfully")
        else:
            await interaction.response.send_message(f"Scoreboard failed to add points for the battle")

    @app_commands.command(name="scoreboard_trade", description="Add a trade to the scoreboard")
    @app_commands.describe(trainer_one='Trainers to choose from', trainer_two='Trainers to choose from', season='Seasons to choose from')
    async def scoreboard_trade(self, interaction: discord.Interaction, trainer_one: str, trainer_two: str, season: str = None):
        is_updated = await JimBotService.scoreboard_trade(trainer_one, trainer_two, season)
        
        if is_updated:
            seasonName = "active season" if season is None else season
            await interaction.response.send_message(f"Scoreboard added 10 Points for a trade to {trainer_one} and {trainer_two} for the {seasonName} succesfully")
        else:
            await interaction.response.send_message(f"Scoreboard failed to add points for the trade")

    @app_commands.command(name="scoreboard_attendance", description="Add an attendance to the scoreboard")
    @app_commands.describe(trainer='Trainers to choose from', season='Seasons to choose from')
    async def scoreboard_attendance(self, interaction: discord.Interaction, trainer: str, season: str = None):
        is_updated = await JimBotService.scoreboard_attendance(trainer, season)
        
        if is_updated:
            seasonName = "active season" if season is None else season
            await interaction.response.send_message(f"Scoreboard added 10 Points for attendance to {trainer} for the {seasonName} succesfully")
        else:
            await interaction.response.send_message(f"Scoreboard failed to add points for attendance")

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
    @scoreboard_attendance.autocomplete('trainer')
    async def trainers_autocomplete(self, interaction: discord.Interaction, current: str):
        trainer_choices = self.get_trainer_choices()
        return [app_commands.Choice(name=trainer_choice.name, value=trainer_choice.value) for trainer_choice in trainer_choices if current.lower() in trainer_choice.name.lower()]

    @scoreboard_battle.autocomplete('season')
    @scoreboard_trade.autocomplete('season')
    @scoreboard_attendance.autocomplete('season')
    @scoreboard_show.autocomplete('season')
    async def seasons_autocomplete(self, interaction: discord.Interaction, current: str):
        season_choices = self.get_season_choices()
        return [app_commands.Choice(name=season_choice.name, value=season_choice.value) for season_choice in season_choices if current.lower() in season_choice.name.lower()]

        
async def setup(bot):
    await bot.add_cog(Scoreboard(bot), guilds=[discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)])