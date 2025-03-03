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

    '''
    print("Create new Trainer for scoreboard")
    print("Add Trainer role to new member")


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

            winner_scoreboard = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=winner))
            looser_scoreboard = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=looser))

            if winner_scoreboard is not None and len(winner_scoreboard) == 1 and looser_scoreboard is not None and len(looser_scoreboard) == 1:
                winner_scoreboard[0].points += 20
                looser_scoreboard[0].points += 10
                data_access.update_scoreboard(winner_scoreboard[0])
                data_access.update_scoreboard(looser_scoreboard[0])
        return True
    except Exception:
        return False

async def scoreboard_trade(trainer_one, trainer_two, season) -> bool:
    try:
        with IDataAccess(_data_access_option) as data_access:
            if season is None:    
                seasons = data_access.read_seasons(Season(is_active = True))
                if seasons is not None and len(seasons) == 1:
                    season = seasons[0].name

            trainer_one_scoreboard = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=trainer_one))
            trainer_two_scoreboard = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=trainer_two))
            
            if trainer_one_scoreboard is not None and len(trainer_one_scoreboard) == 1 and trainer_two_scoreboard is not None and len(trainer_two_scoreboard) == 1:
                trainer_one_scoreboard.points += 10
                trainer_two_scoreboard.points += 10
                data_access.update_scoreboard(trainer_one_scoreboard)
                data_access.update_scoreboard(trainer_two_scoreboard)
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

            trainer_scoreboard = data_access.read_scoreboards(Scoreboard(season_name=season, trainer_discord_name=trainer))
            
            if trainer_scoreboard is not None and len(trainer_scoreboard) == 1:
                trainer_scoreboard[0].points += 10
                data_access.update_scoreboard(trainer_scoreboard[0])
        return True
    except Exception:
        return False

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