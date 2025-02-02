from Models.Season import Season
from Models.Trainer import Trainer
from Models.Scoreboard import Scoreboard
from Models.Enum.DataAccessOption import DataAccessOption
from DataAccess.DataAccessDummy import DataAccessDummy
from DataAccess.DataAccessPostgre import DataAccessPostgre

class IDataAccess():
    def __init__(self, data_access_option:DataAccessOption):
        if data_access_option == DataAccessOption.POSTGRE:
            self._data_access = DataAccessPostgre()
        else:
            self._data_access = DataAccessDummy()

    def __enter__(self):
        self._data_access.start_transaction()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        exc_type: The type of the exception that was raised (e.g., ValueError, TypeError). If no exception was raised, this will be None.
        exc_val: The actual exception instance that was raised. If no exception was raised, this will be None.
        exc_tb: The traceback object associated with the exception. If no exception was raised, this will be None.
        '''
        if exc_type is None:
            self._data_access.commit_transaction()
        else:
            self._data_access.rollback_transaction()


    def create_trainer(self, trainer: Trainer):
        self._data_access.create_trainer(trainer)

    def read_trainers(self, trainer: Trainer) -> list[Trainer]:
        return self._data_access.read_trainers(trainer)

    def update_trainer(self, trainer: Trainer):
        self._data_access.update_trainer(trainer)

    def delete_trainer(self, trainer: Trainer):
        self._data_access.delete_trainer(trainer)


    def create_season(self, season: Season):
        self._data_access.create_season(season)

    def read_seasons(self, season: Season) -> list[Season]:
        return self._data_access.read_seasons(season)

    def update_season(self, season: Season):
        self._data_access.update_season(season)

    def delete_season(self, season: Season):
        self._data_access.delete_season(season)


    def create_scoreboard(self, scoreboard: Scoreboard):
        self._data_access.create_scoreboard(scoreboard)

    def read_scoreboards(self, scoreboard: Scoreboard) -> list[Scoreboard]:
        return self._data_access.read_scoreboards(scoreboard)

    def update_scoreboard(self, scoreboard: Scoreboard):
        self._data_access.update_scoreboard(scoreboard)

    def delete_scoreboard(self, scoreboard: Scoreboard):
        self._data_access.delete_scoreboard(scoreboard)