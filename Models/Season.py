class Season: 
    def __init__(self, name:str = "", badge_points:int = 0, is_active:bool = False): 
        self._name = name
        self._badge_points = badge_points 
        self._is_active = is_active

    def __str__(self):
        status = "active" if self._is_active else "inactive"
        return f"In the {status} {self._name} you need {self._badge_points} for the badge"


    @property
    def name(self): 
        return str(self._name)
    
    @name.setter
    def name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for Name")
        self._name = str(new_value)
    

    @property
    def badge_points(self): 
        return int(self._badge_points)
    
    @badge_points.setter
    def badge_points(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Expected an int for BadgePoints")
        self._badge_points = int(new_value) 
    

    @property
    def is_active(self): 
        return bool(self._is_active)
    
    @is_active.setter
    def is_active(self, new_value):
        if not isinstance(new_value, bool):
            raise TypeError("Expected a boolean for IsActive")
        self._is_active = bool(new_value)