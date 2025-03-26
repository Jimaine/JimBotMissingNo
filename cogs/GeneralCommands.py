import Service.JimBotService as JimBotService
import discord
from discord import app_commands
from discord.ext import commands
from Models.JimBotSecrets import JimBotSecrets


jim_bot_secrets = JimBotSecrets()

class GeneralCommands(commands.Cog):
    # initialize GeneralCommands
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('GeneralCommands cog loaded')


    # commands
    @commands.command()
    async def sync(self, context) -> None:
        try:
            fmt = await context.bot.tree.sync(guild=context.guild)
            await context.send(
                f"MISSINGNO Synced {len(fmt)} commands to the current guild"
            )
        except Exception as exception:
            await context.send(
                f"Exception while syncing {exception}"
            )
        return


    # app commands
    @app_commands.command(name="help", description="get help with the bot")
    async def help(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(
            """
                **Commands**
                .sync - Syncs the commands to the current guild
                **Slash Commands**
                /help - Get help with the bot
                /trainer_add - Add a new trainer
                /trainer_set_name - Set the name of a trainer
                /trainer_set_is_active - Set activity of a trainer
                /season_add - Add a new season
                /season_activate - Activate a season
                /scoreboard_battle - Add a battle to the scoreboard
                /scoreboard_trade - Add a trade to the scoreboard
                /scoreboard_show - Add a trade to the scoreboard     
            """.replace("                ", "")
        )

        
async def setup(bot):
    await bot.add_cog(GeneralCommands(bot), guilds=[discord.Object(id=jim_bot_secrets.discord_missing_no_guild_id),discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)])