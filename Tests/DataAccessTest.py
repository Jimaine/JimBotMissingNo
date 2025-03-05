from Models.Enum.DataAccessOption import DataAccessOption
from DataAccess.IDataAccess import IDataAccess
from Models.Season import Season
from Models.Trainer import Trainer
from Models.Scoreboard import Scoreboard

def test_data_access():
    with IDataAccess(DataAccessOption.DUMMY) as transaction:
        test_data_access_for_one_option(transaction)
        
    with IDataAccess(DataAccessOption.POSTGRE) as transaction:
        test_data_access_for_one_option(transaction)

def test_data_access_for_one_option(dataAccess:IDataAccess):
    # Get all trainers before test begins
    trainers = dataAccess.read_trainers(None)
    print(f"Trainer: {len(trainers)}")

    # Get all seasons before test begins
    seasons = dataAccess.read_seasons(None)
    print(f"Season: {len(seasons)}")

    # Get all scoreboards before test begins
    scoreboards = dataAccess.read_scoreboards(None)
    print(f"Scoreboard: {len(scoreboards)}")


    # Create a new trainer
    trainer_discord_name = "MistyAzuria"
    trainer = dataAccess.create_trainer(Trainer(discord_name = trainer_discord_name, created_by = "Dummy"))
    trainers = dataAccess.read_trainers(None)
    print(f"Trainer: {len(trainers)}")

    # Update the trainer
    trainer = dataAccess.read_trainers(Trainer(discord_name = trainer_discord_name))
    trainer[0].name = "Misty"
    trainer[0].is_active = True
    dataAccess.update_trainer(trainer[0])
    trainers = dataAccess.read_trainers(None)
    print(f"Trainer: {len(trainers)}")

    # Create a new season
    season_name = "Azuria City Season"
    season = dataAccess.create_season(Season(name = season_name, created_by = "Dummy"))
    seasons = dataAccess.read_seasons(None)
    print(f"Season: {len(seasons)}")

    # Update the season
    season = dataAccess.read_seasons(Season(name = season_name))
    season[0].badge_points = 300
    season[0].is_active = True
    dataAccess.update_season(season[0])
    seasons = dataAccess.read_seasons(None)
    print(f"Season: {len(seasons)}")
    
    # Create a new scoreboard
    dataAccess.create_scoreboard(Scoreboard(season_name, trainer_discord_name, created_by = "Dummy"))
    scoreboards = dataAccess.read_scoreboards(None)
    print(f"Scoreboard: {len(scoreboards)}")

    # Update the scoreboard
    scoreboard = dataAccess.read_scoreboards(Scoreboard(season_name, trainer_discord_name))
    scoreboard[0].points = 100
    dataAccess.update_scoreboard(scoreboard[0])
    scoreboards = dataAccess.read_scoreboards(None)
    print(f"Scoreboard: {len(scoreboards)}")


    # Delete the scoreboard
    dataAccess.delete_scoreboard(Scoreboard(season_name, trainer_discord_name))
    scoreboards = dataAccess.read_scoreboards(None)
    print(f"Scoreboard: {len(scoreboards)}")

    # Delete the season
    dataAccess.delete_season(Season(name = season_name))
    seasons = dataAccess.read_seasons(None)
    print(f"Season: {len(seasons)}")

    # Delete the trainer
    dataAccess.delete_trainer(Trainer(discord_name = trainer_discord_name))
    trainers = dataAccess.read_trainers(None)
    print(f"Trainer: {len(trainers)}")

    '''
    trainer = JimBotDataAccess.read_trainer(discordName)
    if trainer is not None:
        trainer.Name = seasonName
        print(JimBotDataAccess.update_trainer(trainer))
    trainers = JimBotDataAccess.read_all_trainer()
    print(len(trainers))
	

    season = JimBotDataAccess.read_season(seasonName)
    if season is not None:
        season.Name = seasonName
        print(JimBotDataAccess.update_trainer(season))
    seasons = JimBotDataAccess.read_all_seasons()
    print(seasons)
	

    scoreboard = JimBotDataAccess.read_scoreboard(seasonName)
    if scoreboard is not None:
        scoreboard.SeasonName = seasonName
        print(JimBotDataAccess.update_scoreboard(scoreboard))
    scoreboards = JimBotDataAccess.read_all_scoreboards()
    print(scoreboards)
    '''