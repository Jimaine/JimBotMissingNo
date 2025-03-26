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
        print('General commands ready')


    # commands
    @commands.command()
    async def sync(self, context) -> None:
        try:
            fmt = await context.bot.tree.sync(guild=context.guild)
            await context.send(
                f"MISSINGNO synchronisiert {len(fmt)} Attacken mit dem Discord Server"
            )
        except Exception as exception:
            await context.send(
                f"Ausnahme verursacht während synchronisation {exception}"
            )
        return


    # app commands
    @app_commands.command(name="hilfsmechanik", description="Listet alle Attacken von MISSINGNO auf")
    async def hilfsmechanik(self, interaction: discord.Interaction):
        service_result = await JimBotService.help()     
        await interaction.response.send_message(str(service_result))
        
        
async def setup(bot):
    await bot.add_cog(
        GeneralCommands(bot), 
        guilds=[
            discord.Object(id=jim_bot_secrets.discord_missing_no_guild_id),
            discord.Object(id=jim_bot_secrets.discord_missing_no_test_guild_id)
        ]
    )