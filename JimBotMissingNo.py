import os
import discord
import asyncio
import Tests.DataAccessTest as DataAccessTest
import Service.JimBotService as JimBotService
from discord.ext import commands
from Models.JimBotSecrets import JimBotSecrets


# Test Data Access
#DataAccessTest.test_data_access()

# initialize secrets
jim_bot_secrets = JimBotSecrets()

# initialize bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents, default_guild_ids=[jim_bot_secrets.discord_missing_no_guild_id, jim_bot_secrets.discord_missing_no_test_guild_id])

# bot events
@bot.event
async def on_ready():
    print("EIN WILDES MISSINGNO ERSCHEINT!")

@bot.event
async def on_member_join(member):
    await JimBotService.on_member_join(member)

# start bot
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(jim_bot_secrets.discord_missing_no_token)

asyncio.run(main())