from Models.Season import Season
from Models.Trainer import Trainer
from Models.Scoreboard import Scoreboard


class DataAccessDummy():
    def __init__(self):
        self._trainers = [Trainer]
        self._trainers = []
        self._seasons = [Season]
        self._seasons = []
        self._scoreboards = [Scoreboard]
        self._scoreboards = []

        self.start_transaction()
        self.create_trainer(Trainer(discord_name = "AshKetchum", name = "Ash",is_active = True))
        self.create_season(Season(name = "Mamoria City Season", badge_points = 370, is_active = True))
        self.create_scoreboard(Scoreboard(season_name = "Mamoria City Season", trainer_discord_name = "AshKetchum", points = 420))
        self.commit_transaction()


    def start_transaction(self):
        self._transaction_trainers = self._trainers
        self._transaction_seasons = self._seasons
        self._transaction_scoreboards = self._scoreboards

    def commit_transaction(self):
        self._trainers = self._transaction_trainers
        self._seasons = self._transaction_seasons
        self._scoreboards = self._transaction_scoreboards
        self._transaction_trainers = None
        self._transaction_seasons = None
        self._transaction_scoreboards = None

    def rollback_transaction(self):
        self._transaction_trainers = None
        self._transaction_seasons = None
        self._transaction_scoreboards = None


    def create_trainer(self, trainer: Trainer):
        self._transaction_trainers.append(trainer)

    def read_trainers(self, trainer: Trainer) -> list[Trainer]:
        if trainer is None:
            return self._transaction_trainers
        if trainer is not None:
            trainers = []
            searchDiscordName = len(trainer.discord_name.strip()) > 0
            searchName = len(trainer.name.strip()) > 0
            searchIsActive = trainer.is_active == True
            for _trainer in self._transaction_trainers:
                if (
                        (searchDiscordName == False or _trainer.discord_name == trainer.discord_name)
                        and (searchName == False or _trainer.name == trainer.name)
                        and (searchIsActive == False or _trainer.is_active == trainer.is_active)
                        ):
                    trainers.append(_trainer)

            return trainers

    def update_trainer(self, trainer: Trainer):
        for _trainer in self._transaction_trainers:
            if _trainer.discord_name == trainer.discord_name:
                _trainer = trainer

    def delete_trainer(self, trainer: Trainer):
        for _trainer in self._transaction_trainers:
            if _trainer.discord_name == trainer.discord_name:
                self._transaction_trainers.remove(_trainer)


    def create_season(self, season: Season):
        self._transaction_seasons.append(season)

    def read_seasons(self, season: Season) -> list[Season]:
        if season is None:
            return self._transaction_seasons
        if season is not None:
            seasons = []
            searchName = len(season.name.strip()) > 0
            searchBadgePoints = season.badge_points > 0
            searchIsActive = season.is_active == True
            for _season in self._transaction_seasons:
                if (
                        (searchName == False or _season.name == season.name)
                        and (searchBadgePoints == False or _season.badge_points == season.badge_points)
                        and (searchIsActive == False or _season.is_active == season.is_active)
                        ):
                    seasons.append(_season)

            return seasons

    def update_season(self, season: Season):
        for _season in self._transaction_seasons:
            if _season.name == season.name:
                _season = season

    def delete_season(self, season: Season):
        for _season in self._transaction_seasons:
            if _season.name == season.name:
                self._transaction_seasons.remove(_season)


    def create_scoreboard(self, scoreboard: Scoreboard):
        self._transaction_scoreboards.append(scoreboard)

    def read_scoreboards(self, scoreboard: Scoreboard) -> list[Scoreboard]:
        if scoreboard is None:
            return self._transaction_scoreboards
        if scoreboard is not None:
            scoreboards = []
            searchSeasonName = len(scoreboard.season_name.strip()) > 0
            searchTrainerDiscordName = len(scoreboard.trainer_discord_name.strip()) > 0
            searchIsActive = scoreboard.points > 0
            for _scoreboard in self._transaction_scoreboards:
                if (
                        (searchSeasonName == False or _scoreboard.season_name == scoreboard.season_name)
                        and (searchTrainerDiscordName == False or _scoreboard.trainer_discord_name == scoreboard.trainer_discord_name)
                        and (searchIsActive == False or _scoreboard.points == scoreboard.points)
                        ):
                    scoreboards.append(_scoreboard)

            return scoreboards

    def update_scoreboard(self, scoreboard: Scoreboard):
        for _scoreboard in self._transaction_scoreboards:
            if _scoreboard.season_name == scoreboard.season_name and _scoreboard.trainer_discord_name == scoreboard.trainer_discord_name:
                _scoreboard = scoreboard

    def delete_scoreboard(self, scoreboard: Scoreboard):
        for _scoreboard in self._transaction_scoreboards:
            if _scoreboard.season_name == scoreboard.season_name and _scoreboard.trainer_discord_name == scoreboard.trainer_discord_name:
                self._transaction_scoreboards.remove(_scoreboard)