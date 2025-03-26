import Service.JimBotService as JimBotService
import discord
from discord import app_commands
from discord.ext import commands
from Models.JimBotSecrets import JimBotSecrets


jim_bot_secrets = JimBotSecrets()

class TrainerCommands(commands.Cog):
    # initialize TrainerCommands
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Trainer commands ready')

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
    
    # app commands
    @app_commands.command(name="trainer_hinzufuegen", description="Fuege einen neuen Pokemon Trainer hinzu")
    @app_commands.describe(discord_name='Der discord Benutzername (Nicht der Anzeigename!)', trainer_name='Der Pokemon Trainer Name')
    async def trainer_hinzufuegen(self, interaction: discord.Interaction, discord_name: str, trainer_name: str = None):
        service_result = await JimBotService.trainer_add(discord_name, created_by = interaction.user.name)
        
        await interaction.response.send_message(str(service_result))
        if trainer_name is not None:
            service_result = await JimBotService.trainer_update_name(discord_name, trainer_name)
            await interaction.response.send_message(str(service_result))

    @app_commands.command(name="trainer_name_aendern", description="Setze den Namen eines Pokemon Trainers")
    @app_commands.describe(alle_trainer='Alle erfassten Pokemon Trainer', neuer_trainer_name='Der neue Pokemon Trainer Name')
    async def trainer_name_aendern(self, interaction: discord.Interaction, alle_trainer: str, neuer_trainer_name: str):
        service_result = await JimBotService.trainer_update_name(alle_trainer, neuer_trainer_name)
        await interaction.response.send_message(str(service_result))
            
    @app_commands.command(name="trainer_aktivitaet_setzen", description="Ist der Pokemon Trainer in-/aktiv?")
    @app_commands.describe(alle_trainer='Alle erfassten Pokemon Trainer', ist_aktiv='Ist Trainer aktiv?')
    async def trainer_aktivitaet_setzen(self, interaction: discord.Interaction, alle_trainer: str, ist_aktiv: str):
        ist_aktiv = True if ist_aktiv == "True" else False
        service_result = await JimBotService.trainer_update_isActive(alle_trainer, ist_aktiv)
        await interaction.response.send_message(str(service_result))

    # autocompletes
    @trainer_aktivitaet_setzen.autocomplete('alle_trainer')
    @trainer_name_aendern.autocomplete('alle_trainer')
    async def trainers_autocomplete(self, interaction: discord.Interaction, current: str):
        trainer_choices = self.get_trainer_choices()
        return [app_commands.Choice(name=trainer_choice.name, value=trainer_choice.value) for trainer_choice in trainer_choices if current.lower() in trainer_choice.name.lower()]

    @trainer_aktivitaet_setzen.autocomplete('ist_aktiv')
    async def is_active_autocomplete(self, interaction: discord.Interaction, current: str):
        is_active_choices = self.get_is_active_choices()
        return [app_commands.Choice(name=is_active_choice.name, value=is_active_choice.value) for is_active_choice in is_active_choices if current.lower() in is_active_choice.name.lower()]

        
async def setup(bot):
    await bot.add_cog(
        TrainerCommands(bot), 
        guilds=[
            discord.Object(id=jim_bot_secrets.discord_missing_no_guild_id),
            discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)
        ]
    )
