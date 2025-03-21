import Service.JimBotService as JimBotService
import discord
from discord import app_commands
from discord.ext import commands
from Models.JimBotSecrets import JimBotSecrets


jim_bot_secrets = JimBotSecrets()

class Season(commands.Cog):
    # initialize season
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Season cog loaded')

    # static methods    
    @staticmethod
    def get_season_choices():
        season_choices = []
        
        for name, value in JimBotService.get_season_choices(is_only_active_season = False).items():
            season_choices.append(discord.app_commands.Choice(name=name, value=value))

        return season_choices

    # commands
    @commands.command()
    async def sync_season(self, context) -> None:
        try:
            fmt = await context.bot.tree.sync(guild=context.guild)
            await context.send(
                f"Synced {len(fmt)} season commands to the current guild"
            )
        except Exception as exception:
            await context.send(
                f"Exception while syncing {exception}"
            )
        return

    # app commands
    @app_commands.command(name="season_add", description="add a new season")
    @app_commands.describe(name='The name of the new season', badge_points='The points for the badge of the new season')
    async def season_add(self, interaction: discord.Interaction, name: str, badge_points: int):
        service_result = await JimBotService.season_add(name, badge_points, created_by = interaction.user.name)
        await interaction.response.send_message(str(service_result))

    @app_commands.command(name="season_activate", description="activate a season")
    @app_commands.describe(seasons='The name of the active season')
    async def season_activate(self, interaction: discord.Interaction, seasons: str):
        service_result = await JimBotService.season_activate(seasons)
        await interaction.response.send_message(str(service_result))

    # autocompletes
    @season_activate.autocomplete('seasons')
    async def seasons_autocomplete(self, interaction: discord.Interaction, current: str):
        season_choices = self.get_season_choices()
        return [app_commands.Choice(name=season_choice.name, value=season_choice.value) for season_choice in season_choices if current.lower() in season_choice.name.lower()]

        
async def setup(bot):
    await bot.add_cog(Season(bot), guilds=[discord.Object(id=jim_bot_secrets.discord_missing_no_guild_id),discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)])