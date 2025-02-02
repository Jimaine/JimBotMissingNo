class Trainer: 
    def __init__(self, discord_name:str = "", name:str = "", is_active:bool = False): 
        self._discord_name = discord_name 
        self._name = name
        self._is_active = is_active

    def __str__(self):
        status = "active" if self._is_active else "inactive"
        return f"The {status} discord user {self._discord_name} is the trainer {self._name}"
    

    @property
    def discord_name(self): 
        return str(self._discord_name)
    
    @discord_name.setter
    def discord_name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for DiscordName")
        self._discord_name = str(new_value) 
    

    @property
    def name(self): 
        return str(self._name)
    
    @name.setter
    def name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for Name")
        self._name = str(new_value) 
    

    @property
    def is_active(self): 
        return bool(self._is_active)
    
    @is_active.setter
    def is_active(self, new_value):
        if not isinstance(new_value, bool):
            raise TypeError("Expected a boolean for IsActive")
        self._is_active = bool(new_value)