from dotenv import load_dotenv
import os 
  

class JimBotSecrets: 
    def __init__(self): 
        load_dotenv()
        self._discord_missing_no_token = os.getenv('DISCORD_MISSING_NO_TOKEN')
        self._discord_missing_no_guild_id = os.getenv('DISCORD_MISSING_NO_GUILD_ID')
        self._discord_missing_no_test_guild_id = os.getenv('DISCORD_MISSING_NO_TEST_GUILD_ID')
        self._postgre_missing_no_host = os.getenv('POSTGRE_MISSING_NO_HOST')
        self._postgre_missing_no_database = os.getenv('POSTGRE_MISSING_NO_DATABASE')
        self._postgre_missing_no_user = os.getenv('POSTGRE_MISSING_NO_USER')
        self._postgre_missing_no_password = os.getenv('POSTGRE_MISSING_NO_PASSWORD')
        self._postgre_missing_no_port = os.getenv('POSTGRE_MISSING_NO_PORT')
    
    @property
    def discord_missing_no_token(self): 
        return str(self._discord_missing_no_token)
    
    @property
    def discord_missing_no_guild_id(self): 
        return int(self._discord_missing_no_guild_id)
    
    @property
    def discord_missing_no_test_guild_id(self): 
        return int(self._discord_missing_no_test_guild_id)
    
    @property
    def postgre_missing_no_host(self): 
        return str(self._postgre_missing_no_host)
    
    @property
    def postgre_missing_no_database(self): 
        return str(self._postgre_missing_no_database)
    
    @property
    def postgre_missing_no_user(self): 
        return str(self._postgre_missing_no_user)
    
    @property
    def postgre_missing_no_password(self): 
        return str(self._postgre_missing_no_password)
    
    @property
    def postgre_missing_no_port(self): 
        return str(self._postgre_missing_no_port)