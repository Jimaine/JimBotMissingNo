from datetime import datetime, timedelta
from Models.Enum.DataAccessOption import DataAccessOption
from Models.Enum.ScoreboardAction import ScoreboardAction
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
async def trainer_add(discord_name: str, created_by: str) -> bool:
    try:
        with IDataAccess(_data_access_option) as data_access:
            data_access.create_trainer(Trainer(discord_name, is_active = True, created_by = created_by))
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
        return True
    except Exception:
        return False


# season methods
async def season_add(name: str, badge_points: int, created_by: str):
    try:
        with IDataAccess(_data_access_option) as data_access:
            data_access.create_season(Season(name, badge_points, created_by = created_by))
        return True
    except Exception:
        return False

async def season_activate(name: str):
    try:
        with IDataAccess(_data_access_option) as data_access:
            seasons = data_access.read_seasons(None)
            for season in seasons:
                season.is_active = True if season.name == name else False
                data_access.update_season(season)
            seasons = data_access.read_seasons(Season(is_active = True))
            return len(seasons) == 1
    except Exception:
        return False


# scoreboard methods
async def scoreboard_battle(winner: str, looser: str, created_by: str) -> bool:
    try:
        if winner == looser:
            return False
        
        with IDataAccess(_data_access_option) as data_access:
            season = await get_season_if_none(data_access)

            data_access.create_scoreboard(Scoreboard(season, trainer_discord_name = winner, action = ScoreboardAction.BATTLE_WIN, created_by = created_by))
            data_access.create_scoreboard(Scoreboard(season, trainer_discord_name = looser, action = ScoreboardAction.BATTLE_LOOSE, created_by = created_by))

            await scoreboard_attendance(data_access = data_access, trainer = winner, season = season, created_by = created_by)
            await scoreboard_attendance(data_access = data_access, trainer = looser, season = season, created_by = created_by)
        return True
    except Exception:
        return False

async def scoreboard_trade(trainer_one: str, trainer_two: str, created_by: str) -> bool:
    try:
        if trainer_one == trainer_two:
            return False
        
        last_season_week_begin = get_last_season_week_begin()

        with IDataAccess(_data_access_option) as data_access: 
            season = await get_season_if_none(data_access)
            
            scoreboards = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=trainer_one, action = ScoreboardAction.TRADE))          
            if any(scoreboard.created_at > last_season_week_begin for scoreboard in scoreboards) == False:
                data_access.create_scoreboard(Scoreboard(season, trainer_discord_name = trainer_one, action = ScoreboardAction.TRADE, created_by = created_by))
                await scoreboard_attendance(data_access = data_access, trainer = trainer_one, season = season, created_by = created_by)

            scoreboards = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=trainer_two, action = ScoreboardAction.TRADE))
            if any(scoreboard.created_at > last_season_week_begin for scoreboard in scoreboards) == False:
                data_access.create_scoreboard(Scoreboard(season, trainer_discord_name = trainer_two, action = ScoreboardAction.TRADE, created_by = created_by))
                await scoreboard_attendance(data_access = data_access, trainer = trainer_two, season = season, created_by = created_by)
        return True
    except Exception:
        return False
    
async def scoreboard_show(season: str) -> str:
    scoreboard_results = ""
    try:
        with IDataAccess(_data_access_option) as data_access:
            season = await get_season_if_none(data_access, season)
            scoreboard_results = f"## {season}:\n\n"
            trainer_scoreboards = data_access.read_scoreboards(Scoreboard(season_name=season))

            if trainer_scoreboards is not None and len(trainer_scoreboards) > 0:
                trainer_scoreboards = group_season_trainer_sum_points(trainer_scoreboards)
                trainer_scoreboards = sorted(trainer_scoreboards, key=lambda trainer_scoreboard: trainer_scoreboard.points, reverse=True)
                for trainer_scoreboard in trainer_scoreboards:
                    trainers = data_access.read_trainers(Trainer(discord_name = trainer_scoreboard.trainer_discord_name))
                    if trainers is not None and len(trainers) == 1:
                        scoreboard_results += f"**{trainers[0].name}** *({trainers[0].discord_name})*: {trainer_scoreboard.points}\n"
    except Exception:
        scoreboard_results = "Scoreboard failed to show results"

    return scoreboard_results

# helper methods
async def scoreboard_attendance(data_access: IDataAccess, trainer: str, season: str, created_by: str) -> bool:
    try:
        last_season_week_begin = get_last_season_week_begin()
        scoreboards = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=trainer, action = ScoreboardAction.ATTENDANCE))
        
        if any(scoreboard.created_at > last_season_week_begin for scoreboard in scoreboards) == False:
            data_access.create_scoreboard(Scoreboard(season, trainer_discord_name = trainer, action = ScoreboardAction.ATTENDANCE, created_by = created_by))
        return True
    except Exception:
        return False
    
async def get_season_if_none(data_access: IDataAccess, season: str = None) -> str:
    if season is None:
        seasons = data_access.read_seasons(Season(is_active = True))
        if seasons is not None and len(seasons) == 1:
            season = seasons[0].name
    return season
    
def get_last_season_week_begin() -> datetime:
    today = datetime.now()
    timedelta_to_last_season_week_begin = timedelta(days=today.weekday()) 
    return today - timedelta_to_last_season_week_begin

def group_season_trainer_sum_points(scoreboards: list[Scoreboard]) -> list[Scoreboard]:
    grouped_scoreboards = {}
    for scoreboard in scoreboards:
        key = (scoreboard.season_name, scoreboard.trainer_discord_name)
        if key not in grouped_scoreboards:
            grouped_scoreboards[key] = Scoreboard(
                season_name=scoreboard.season_name,
                trainer_discord_name=scoreboard.trainer_discord_name
            )
        grouped_scoreboards[key].points += scoreboard.points
    return list(grouped_scoreboards.values())