import Service.JimBotService as JimBotService
import discord
from discord import app_commands
from discord.ext import commands
from Models.JimBotSecrets import JimBotSecrets


jim_bot_secrets = JimBotSecrets()

class Trainer(commands.Cog):
    # initialize trainer
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Trainer cog loaded')

    # static methods
    @staticmethod
    def get_trainer_choices():
        trainer_choices = []
        
        for name, value in JimBotService.get_trainer_choices(is_only_active_trainers = False).items():
            trainer_choices.append(discord.app_commands.Choice(name=name, value=value))

        return trainer_choices
    
    @staticmethod
    def get_is_active_choices():
        is_active_choices = []
        
        for name, value in JimBotService.get_is_active_choices().items():
            is_active_choices.append(discord.app_commands.Choice(name=name, value=value))

        return is_active_choices
          
    # commands
    @commands.command()
    async def sync_trainer(self, context) -> None:
        try:
            fmt = await context.bot.tree.sync(guild=context.guild)
            await context.send(
                f"Synced {len(fmt)} trainer commands to the current guild"
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
        is_created = await JimBotService.trainer_add(discord_name, created_by = interaction.user.name)
        
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
        is_updated = await JimBotService.trainer_update_isActive(trainers, is_active, created_by = interaction.user.name)
        
        if is_updated:
            status = "activated" if is_active else "deactivated"
            await interaction.response.send_message(f"User {trainers} successfully {status}")
        else:
            await interaction.response.send_message(f"Activity change of user {trainers} failed")

    # autocompletes
    @trainer_set_is_active.autocomplete('trainers')
    @trainer_set_name.autocomplete('trainers')
    async def trainers_autocomplete(self, interaction: discord.Interaction, current: str):
        trainer_choices = self.get_trainer_choices()
        return [app_commands.Choice(name=trainer_choice.name, value=trainer_choice.value) for trainer_choice in trainer_choices if current.lower() in trainer_choice.name.lower()]

    @trainer_set_is_active.autocomplete('is_active')
    async def is_active_autocomplete(self, interaction: discord.Interaction, current: str):
        is_active_choices = self.get_is_active_choices()
        return [app_commands.Choice(name=is_active_choice.name, value=is_active_choice.value) for is_active_choice in is_active_choices if current.lower() in is_active_choice.name.lower()]

        
async def setup(bot):
    await bot.add_cog(Trainer(bot), guilds=[discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)])