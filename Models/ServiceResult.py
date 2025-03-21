class ServiceResult: 
    def __init__(self, method_name:str = "", message:str = "", is_successful:bool = True): 
        self._method_name = method_name 
        self._message = message 
        self._is_successful = is_successful

    def __str__(self):
        status = "DATENBANK ist besschrieben!" if self._is_successful else "Keine Wirkung auf DATENBANK!"
        return f"MISSINGNO benutzt {self._method_name} gegen DATENBANK\r\n{self.message}\r\n{status}"


    @property
    def method_name(self): 
        return str(self._method_name)
    
    @method_name.setter
    def method_name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for method_name")
        self._method_name = str(new_value) 


    @property
    def message(self): 
        return str(self._message)
    
    @message.setter
    def message(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Expected a string for message")
        self._message = str(new_value) 

        
    @property
    def is_successful(self): 
        return bool(self._is_successful)
    
    @is_successful.setter
    def is_successful(self, new_value):
        if not isinstance(new_value, bool):
            raise TypeError("Expected a boolean for is_successful")
        self._is_successful = bool(new_value)
    