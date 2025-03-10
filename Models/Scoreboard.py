from Models.Enum.ScoreboardAction import ScoreboardAction
from datetime import datetime


class Scoreboard: 
    def __init__(self, season_name:str = "", trainer_discord_name:str = "", action:ScoreboardAction = ScoreboardAction.NONE, points:int = 0, created_by:str = "", created_at: datetime = None): 
        self._season_name = season_name
        self._trainer_discord_name = trainer_discord_name
        self._action = action
        self._points = points
        self._created_by = created_by
        self._created_at = created_at

    def __str__(self):
        return f"In {self._season_name} the user {self._trainer_discord_name} got {self._points} points"

    @property
    def trainer_discord_name(self): 
        return str(self._trainer_discord_name)
    
    @trainer_discord_name.setter
    def trainer_discord_name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for trainer_discord_name")
        self._trainer_discord_name = str(new_value)
    

    @property
    def season_name(self): 
        return str(self._season_name)
    
    @season_name.setter
    def season_name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for season_name")
        self._season_name = str(new_value)
    

    @property
    def action(self): 
        return ScoreboardAction(self._action)
    
    @action.setter
    def action(self, new_value):
        if not isinstance(new_value, ScoreboardAction):
            raise TypeError("Expected a string for action")
        self._action = ScoreboardAction(new_value)
    

    @property
    def points(self): 
        return int(self._points)
    
    @points.setter
    def points(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Expected an int for points")
        self._points = int(new_value) 


    @property
    def created_by(self): 
        return str(self._created_by)
    
    @created_by.setter
    def created_by(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for created_by")
        self._created_by = str(new_value) 


    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, new_value):
        if not isinstance(new_value, datetime):
            raise TypeError("Expected a datetime object for created_at")
        self._created_at = new_value