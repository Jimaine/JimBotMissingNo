import os
import discord
import asyncio
import Tests.DataAccessTest as DataAccessTest
from discord import app_commands
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

@bot.event
async def on_ready():
    print("A WILD MISSING NO APPEARS")

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(jim_bot_secrets.discord_missing_no_token)

asyncio.run(main())


'''
# initialize slash options
seasons_choices = discord.SlashOption(description="all seasons", required=True, choices=JimBotService.get_season_choices())
seasons_optional_choices = discord.SlashOption(description="all seasons", required=False, choices=JimBotService.get_season_choices())
trainer_active_choices = discord.SlashOption(description="all active trainers", required=True, choices=JimBotService.get_trainer_choices(is_only_active_trainers=True))
    
@bot.event
async def on_member_join(member):
    await JimBotService.on_ready(member)

@bot.slash_command()
async def season(interaction: discord.Interaction):
    pass

@season.subcommand(name="add", description = "add a new season")
async def season_add(interaction: discord.Interaction, name: str, badge_points: int):
    is_created = await JimBotService.season_add(name, badge_points)
    
    if is_created:
        await interaction.response.send_message(f"Season {name} created successfully")
    else:
        await interaction.response.send_message(f"Creating season {name} faild")

@season.subcommand(name="activate", description = "activate a season")
async def season_activate(interaction: discord.Interaction, name = seasons_choices):
    is_updated = await JimBotService.season_activate(name)
    
    if is_updated:
        await interaction.response.send_message(f"Season {name} succesfully is now the active season")
    else:
        await interaction.response.send_message(f"Activity change of season {name} faild")

@bot.slash_command()
async def scoreboard(interaction: discord.Interaction):
    pass

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


@bot.slash_command(guild_ids=[1325798483554467934], name="add", description = "add a new trainer")
async def add(interaction : discord.Interaction, discordName):
    await JimBotService.trainer_add(interaction, discordName)

async def refresh_SlashOptions():
    seasons = JimBotService.get_seasons()
    winners = JimBotService.get_winners()
    loosers = JimBotService.get_loosers()

@bot.event
async def on_message(message):
    username = message.author.display_name
    if message.author == bot.user:
        return

    if message.content == "hello":
        await message.channel.send(f"hi {username}")

@bot.event
async def on_member_join(member):
    guild = member.guild
    guildName = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"Welcome to {guildName}, {member.name}!")

@bot.event
async def on_raw_reaction_add(payload):
    messageId = payload.message_id

    if messageId == 1327320666084605963:
        emoji = payload.emoji.name
        guildId = payload.guild_id
        guild = bot.get_guild(guildId)
        if emoji == "💪":
            role = nextcord.utils.get(guild.roles, name = "muscle")
            if role is not None:
                member = payload.member
                if member is not None:
                    await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    messageId = payload.message_id

    if messageId == 1327320666084605963:
        emoji = payload.emoji.name
        guildId = payload.guild_id
        guild = bot.get_guild(guildId)
        if emoji == "💪":
            role = nextcord.utils.get(guild.roles, name = "muscle")
            if role is not None:
                userId = payload.user_id
                member = guild.get_member(userId) # funktioniert nicht, weil member nicht gefunden wird
                if member is not None:
                    await member.remove_roles(role)
'''