from Models.Enum.DataAccessOption import DataAccessOption
from DataAccess.IDataAccess import IDataAccess
from Models.Season import Season
from Models.Trainer import Trainer
from Models.Scoreboard import Scoreboard


_data_access_option = DataAccessOption.POSTGRE

# get choices for slash options
def get_season_choices(is_only_active_season: bool = False) -> dict:   
    choices = {}
    
    with IDataAccess(_data_access_option) as data_access:
        seasons = data_access.read_seasons(Season(is_active = is_only_active_season))

        for season in seasons:
            choices[season.name] = season.name
    
    return choices

def get_trainer_choices(is_only_active_trainers: bool = False) -> dict:
    choices = {}

    with IDataAccess(_data_access_option) as data_access:
        trainers = data_access.read_trainers(Trainer(is_active = is_only_active_trainers))

        for trainer in trainers:
            choices[f"{trainer.name} ({trainer.discord_name})"] = trainer.discord_name

    return choices

def get_is_active_choices() -> dict:
    choices = {}

    choices["Yes"] = "True"
    choices["No"] = "False"

    return choices

# event methods
async def on_ready():
    print("A WILD MISSING NO APPEARS")
  
async def on_member_join(member):
    '''
    print(member.global_name)
    print(member.display_name)
    print(member.name)
    isCreated = await JimBotDataAccess.create_trainer(member.name)
    if isCreated:
        print("Trainer created")
    else:
        print("Trainer already exists")
    #async await

    @bot.event
    async def on_member_join(member):
        guild = member.guild
        guildName = guild.name
        dmchannel = await member.create_dm()
        await dmchannel.send(f"Welcome to {guildName}, {member.name}!")
    '''
    print("Create new Trainer for scoreboard and add Trainer role to new member")

async def on_message(message):
    '''
    username = message.author.display_name
    if message.author == bot.user:
        return

    if message.content == "hello":
        await message.channel.send(f"hi {username}")
    '''
    print("Do something when a message is received")

async def on_raw_reaction_add(payload):
    '''
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
    '''
    print("Do something when a reaction is added")

async def on_raw_reaction_remove(payload):
    '''
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
    print("Do something when a reaction is removed")

# trainer methods
async def trainer_add(discord_name: str) -> bool:
    try:
        with IDataAccess(_data_access_option) as data_access:
            data_access.create_trainer(Trainer(discord_name, is_active = True))
            await create_scoreboard(data_access, trainer_discord_name = discord_name)
        return True
    except Exception:
        return False

async def trainer_update_name(discord_name: str, trainer_name: str) -> bool:
    try:
        with IDataAccess(_data_access_option) as data_access:
            trainer = data_access.read_trainers(Trainer(discord_name))
            if len(trainer) == 1:
                trainer[0].name = trainer_name
                data_access.update_trainer(trainer[0])
        return True
    except Exception:
        return False

async def trainer_update_isActive(discord_name: str, is_active: bool) -> bool:
    try:
        with IDataAccess(_data_access_option) as data_access:
            trainer = data_access.read_trainers(Trainer(discord_name))
            if len(trainer) == 1:
                trainer[0].is_active = is_active
                data_access.update_trainer(trainer[0])
                if trainer[0].is_active:
                    await create_scoreboard(data_access, trainer_discord_name = discord_name)
        return True
    except Exception:
        return False


# season methods
async def season_add(name, badge_points):
    try:
        with IDataAccess(_data_access_option) as data_access:
            data_access.create_season(Season(name, badge_points))
        return True
    except Exception:
        return False

async def season_activate(name):
    try:
        with IDataAccess(_data_access_option) as data_access:
            seasons = data_access.read_seasons(None)
            for season in seasons:
                season.is_active = True if season.name == name else False
                data_access.update_season(season)
                await create_scoreboard(data_access, season_name = name)
            seasons = data_access.read_seasons(Season(is_active = True))
            return len(seasons) == 1
    except Exception:
        return False


# scoreboard methods
async def scoreboard_battle(winner, looser, season) -> bool:
    try:
        with IDataAccess(_data_access_option) as data_access:
            if season is None:
                seasons = data_access.read_seasons(Season(is_active = True))
                if seasons is not None and len(seasons) == 1:
                    season = seasons[0].name

            winner_scoreboards = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=winner))
            looser_scoreboards = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=looser))

            if winner_scoreboards is not None and len(winner_scoreboards) == 1 and looser_scoreboards is not None and len(looser_scoreboards) == 1:
                winner_scoreboards[0].points += 20
                looser_scoreboards[0].points += 10
                data_access.update_scoreboard(winner_scoreboards[0])
                data_access.update_scoreboard(looser_scoreboards[0])
        return True
    except Exception:
        return False

async def scoreboard_trade(trainer_one, trainer_two, season) -> bool:
    try:
        if trainer_one == trainer_two:
            return False
        
        with IDataAccess(_data_access_option) as data_access:
            if season is None:    
                seasons = data_access.read_seasons(Season(is_active = True))
                if seasons is not None and len(seasons) == 1:
                    season = seasons[0].name

            trainer_one_scoreboards = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=trainer_one))
            trainer_two_scoreboards = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=trainer_two))
            
            if trainer_one_scoreboards is not None and len(trainer_one_scoreboards) == 1 and trainer_two_scoreboards is not None and len(trainer_two_scoreboards) == 1:
                trainer_one_scoreboards[0].points += 10
                trainer_two_scoreboards[0].points += 10
                data_access.update_scoreboard(trainer_one_scoreboards[0])
                data_access.update_scoreboard(trainer_two_scoreboards[0])
        return True
    except Exception:
        return False
    
async def scoreboard_attendance(trainer, season) -> bool:
    try:
        with IDataAccess(_data_access_option) as data_access:
            if season is None:
                seasons = data_access.read_seasons(Season(is_active = True))
                if seasons is not None and len(seasons) == 1:
                    season = seasons[0].name

            trainer_scoreboards = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=trainer))
            
            if trainer_scoreboards is not None and len(trainer_scoreboards) == 1:
                trainer_scoreboards[0].points += 10
                data_access.update_scoreboard(trainer_scoreboards[0])
        return True
    except Exception:
        return False
    
async def scoreboard_show(season) -> str:
    scoreboard_results = ""
    try:
        with IDataAccess(_data_access_option) as data_access:
            if season is None:
                seasons = data_access.read_seasons(Season(is_active = True))
                if seasons is not None and len(seasons) == 1:
                    season = seasons[0].name

            scoreboard_results = f"## {season}:\n\n"
            
            trainer_scoreboards = data_access.read_scoreboards(Scoreboard(season_name=season))
            if trainer_scoreboards is not None and len(trainer_scoreboards) > 0:
                trainer_scoreboards = sorted(trainer_scoreboards, key=lambda trainer_scoreboard: trainer_scoreboard.points, reverse=True)
                for trainer_scoreboard in trainer_scoreboards:
                    trainers = data_access.read_trainers(Trainer(discord_name = trainer_scoreboard.trainer_discord_name))
                    if trainers is not None and len(trainers) == 1:
                        scoreboard_results += f"**{trainers[0].name}** *({trainers[0].discord_name})*: {trainer_scoreboard.points}\n"
    except Exception:
        scoreboard_results = "Scoreboard failed to show results"

    return scoreboard_results

# helper methods
async def create_scoreboard(data_access: IDataAccess, season_name: str = "", trainer_discord_name: str = ""):
    if len(season_name.strip()) <= 0:
        seasons = data_access.read_seasons(Season(is_active = True))
        if len(seasons) == 1:
            season_name = seasons[0].name
        else:
            raise Exception(f"there are {len(seasons)} active seasons.")

    trainers = []
    if len(trainer_discord_name.strip()) > 0:
        trainers.append(Trainer(discord_name = trainer_discord_name))
    else:
        trainers = data_access.read_trainers(Trainer(is_active = True))

    for trainer in trainers:
        scoreboard = Scoreboard(season_name, trainer_discord_name = trainer.discord_name)
        existing_scoreboard_of_trainer = data_access.read_scoreboards(scoreboard)
        if len(existing_scoreboard_of_trainer) == 0:
            data_access.create_scoreboard(scoreboard)