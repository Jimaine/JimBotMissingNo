import Service.JimBotService as JimBotService
import discord
from discord import app_commands
from discord.ext import commands
from Models.JimBotSecrets import JimBotSecrets


jim_bot_secrets = JimBotSecrets()

class Trainer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Trainer cog loaded')

    @commands.command()
    async def syncy(self, ctx) -> None:
        try:
            fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.send(
                f"Synced {len(fmt)} commands to the current guild"
            )
        except Exception as exception:
            await ctx.send(
                f"Exception while syncing {exception}"
            )
        return
    
    @staticmethod
    def get_trainer_choices():
        choices = []
        
        trainers = JimBotService.get_trainer_choices()
        for key, trainerName in trainers.items():
            choices.append(discord.app_commands.Choice(name=key, value=trainerName))

        return choices
    
    # Add the guild ids in which the slash command will appear.
    # If it should be in all, remove the argument, but note that
    # it will take some time (up to an hour) to register the
    # command if it's for all guilds.
    @app_commands.command(name="choosetrainer", description="trainer selector")
    @app_commands.describe(trainers='Trainers to choose from')
    async def choosetrainer(self, interaction: discord.Interaction, trainers: str):
        trainer_choice = next(choice for choice in self.get_trainer_choices() if choice.value == trainers)
        await JimBotService.trainer_add(trainer_choice.value + "O")
        await interaction.response.send_message(f'Hello in {trainer_choice.name}')

    @choosetrainer.autocomplete('trainers')
    async def trainers_autocomplete(self, interaction: discord.Interaction, current: str):
        choices = self.get_trainer_choices()
        return [app_commands.Choice(name=choice.name, value=choice.value) for choice in choices if current.lower() in choice.name.lower()]

        
async def setup(bot):
    await bot.add_cog(Trainer(bot), guilds=[discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)])