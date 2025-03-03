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

    '''
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
    @app_commands.command(name="trainer_add", description="add a new trainer")
    @app_commands.describe(discord_name='The discord name of the new trainer')
    async def trainer_add(self, interaction: discord.Interaction, discord_name: str, trainer_name: str = None):
        is_created = await JimBotService.trainer_add(discord_name)
        
        if is_created:
            await interaction.response.send_message(f"User {discord_name} created successfully")
            if trainer_name is not None:
                await JimBotService.trainer_update_name(discord_name, trainer_name)
        else:
            await interaction.response.send_message(f"Creating user {discord_name} faild")

    @app_commands.command(name="trainer_set_name", description="set the name of a trainer")
    @app_commands.describe(trainers='Trainers to choose from')
    async def trainer_set_name(self, interaction: discord.Interaction, trainers: str, new_trainer_name: str):
        is_updated = await JimBotService.trainer_update_name(trainers, new_trainer_name)

        if is_updated:
            await interaction.response.send_message(f"Trainername of user {trainers} is set to {new_trainer_name}")
        else:
            await interaction.response.send_message(f"Updating the trainername of user {trainers} failed")
            
    @app_commands.command(name="trainer_set_is_active", description="set activity of a trainer")
    @app_commands.describe(trainers='Trainers to choose from', is_active='set is active')
    async def trainer_set_is_active(self, interaction: discord.Interaction, trainers: str, is_active: str):
        is_active = True if is_active == "True" else False
        is_updated = await JimBotService.trainer_update_isActive(trainers, is_active)
        
        if is_updated:
            status = "activated" if is_active else "deactivated"
            await interaction.response.send_message(f"User {trainers} successfully {status}")
        else:
            await interaction.response.send_message(f"Activity change of user {trainers} failed")
    
    @scoreboard.subcommand(name="battle", description = "Add a battle to the scoreboard")
    async def scoreboard_battle(interaction: discord.Interaction, winner = trainer_active_choices, looser = trainer_active_choices, season = seasons_optional_choices):
        is_updated = await JimBotService.scoreboard_battle(winner, looser, season)
        
        if is_updated:
            seasonName = "active season" if season is None else season
            await interaction.response.send_message(f"Scoreboard added 20 Points to {winner} as the winner and 10 Points to the opponent {looser} for the {seasonName} succesfully")
        else:
            await interaction.response.send_message(f"Scoreboard failed to add points for the battle")

    @scoreboard.subcommand(name="trade", description = "Add a trade to the scoreboard")
    async def scoreboard_trade(interaction: discord.Interaction, trainer_one = trainer_active_choices, trainer_two = trainer_active_choices, season = seasons_optional_choices):
        is_updated = await JimBotService.scoreboard_trade(trainer_one, trainer_two, season)
        
        if is_updated:
            seasonName = "active season" if season is None else season
            await interaction.response.send_message(f"Scoreboard added 10 Points for a trade to {trainer_one} and {trainer_two} for the {seasonName} succesfully")
        else:
            await interaction.response.send_message(f"Scoreboard failed to add points for the trade")

    @scoreboard.subcommand(name="attendance", description = "Add an attendance to the scoreboard")
    async def scoreboard_attendance(interaction: discord.Interaction, trainer = trainer_active_choices, season = seasons_optional_choices):
        is_updated = await JimBotService.scoreboard_attendance(trainer, season)
        
        if is_updated:
            seasonName = "active season" if season is None else season
            await interaction.response.send_message(f"Scoreboard added 10 Points for attendance to {trainer} for the {seasonName} succesfully")
        else:
            await interaction.response.send_message(f"Scoreboard failed to add points for attendance")

    # autocompletes
    @trainer_set_is_active.autocomplete('trainers')
    @trainer_set_name.autocomplete('trainers')
    async def trainers_autocomplete(self, interaction: discord.Interaction, current: str):
        trainer_choices = self.get_trainer_choices()
        return [app_commands.Choice(name=trainer_choice.name, value=trainer_choice.value) for trainer_choice in trainer_choices if current.lower() in trainer_choice.name.lower()]

    @trainer_set_name.autocomplete('seasons')
    async def seasons_autocomplete(self, interaction: discord.Interaction, current: str):
        season_choices = self.get_season_choices()
        return [app_commands.Choice(name=season_choice.name, value=season_choice.value) for season_choice in season_choices if current.lower() in season_choice.name.lower()]
    '''

        
async def setup(bot):
    await bot.add_cog(Scoreboard(bot), guilds=[discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)])