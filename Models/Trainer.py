from datetime import datetime


class Trainer: 
    def __init__(self, discord_name:str = "", name:str = "", is_active:bool = False, created_by:str = "", created_at: datetime = None): 
        self._discord_name = discord_name 
        self._name = name
        self._is_active = is_active
        self._created_by = created_by
        self._created_at = created_at

    def __str__(self):
        status = "active" if self._is_active else "inactive"
        return f"The {status} discord user {self._discord_name} is the trainer {self._name}"
    

    @property
    def discord_name(self): 
        return str(self._discord_name)
    
    @discord_name.setter
    def discord_name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for discord_name")
        self._discord_name = str(new_value) 
    

    @property
    def name(self): 
        return str(self._name)
    
    @name.setter
    def name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for name")
        self._name = str(new_value) 
    

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