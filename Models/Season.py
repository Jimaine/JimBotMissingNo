from datetime import datetime


class Season: 
    def __init__(self, name:str = "", badge_points:int = 0, is_active:bool = False, created_by:str = "", created_at: datetime = None): 
        self._name = name
        self._badge_points = badge_points 
        self._is_active = is_active
        self._created_by = created_by
        self._created_at = created_at

    def __str__(self):
        status = "active" if self._is_active else "inactive"
        return f"In the {status} {self._name} you need {self._badge_points} for the badge"


    @property
    def name(self): 
        return str(self._name)
    
    @name.setter
    def name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for name")
        self._name = str(new_value)
    

    @property
    def badge_points(self): 
        return int(self._badge_points)
    
    @badge_points.setter
    def badge_points(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Expected an int for badge_points")
        self._badge_points = int(new_value) 
    

    @property
    def is_active(self): 
        return bool(self._is_active)
    
    @is_active.setter
    def is_active(self, new_value):
        if not isinstance(new_value, bool):
            raise TypeError("Expected a boolean for is_active")
        self._is_active = bool(new_value)


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