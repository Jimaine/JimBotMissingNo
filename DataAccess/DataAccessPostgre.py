from Models.Enum.ScoreboardAction import ScoreboardAction
from Models.Season import Season
from Models.Trainer import Trainer
from Models.Scoreboard import Scoreboard
from Models.JimBotSecrets import JimBotSecrets
import psycopg2


class DataAccessPostgre():
    def __init__(self):
        self.start_transaction()
        with self._connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Trainer (
                    discord_name VARCHAR(100) PRIMARY KEY NOT NULL,
                    name VARCHAR(100),
                    is_active BOOLEAN NOT NULL,
                    created_by VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                );"""
            )
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Season (
                    name VARCHAR(150) PRIMARY KEY NOT NULL,
                    badge_points INT NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    created_by VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                );"""
            )
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Action (
                    name VARCHAR(50) PRIMARY KEY NOT NULL,
                    points INT NOT NULL,
                    created_by VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                );
                INSERT INTO Action (name, points, created_by)
                VALUES ('ATTENDANCE', 10, 'Initial')
                ON CONFLICT (name) DO NOTHING;
                INSERT INTO Action (name, points, created_by)
                VALUES ('TRADE', 10, 'Initial')
                ON CONFLICT (name) DO NOTHING;
                INSERT INTO Action (name, points, created_by)
                VALUES ('BATTLE_WIN', 20, 'Initial')
                ON CONFLICT (name) DO NOTHING;
                INSERT INTO Action (name, points, created_by)
                VALUES ('BATTLE_LOOSE', 10, 'Initial')
                ON CONFLICT (name) DO NOTHING;"""
            )
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Scoreboard (
                    season_name VARCHAR(150) NOT NULL,
                    trainer_discord_name VARCHAR(100) NOT NULL,
                    action_name VARCHAR(50) NOT NULL,
                    created_by VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (season_name) REFERENCES Season(name),
                    FOREIGN KEY (trainer_discord_name) REFERENCES Trainer(discord_name),
                    FOREIGN KEY (action_name) REFERENCES Action(name)
                );
                CREATE INDEX IF NOT EXISTS idx_scoreboard_season_trainer_action ON Scoreboard (
                    season_name, 
                    trainer_discord_name, 
                    action_name
                );"""
            )
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_scoreboard_season_trainer_action ON Scoreboard (
                    season_name, 
                    trainer_discord_name, 
                    action_name
                );"""
            )
        self.commit_transaction()

    def start_transaction(self):
        jimBotSecrets = JimBotSecrets()

        self._connection = psycopg2.connect(
            host=jimBotSecrets.postgre_missing_no_host, 
            database=jimBotSecrets.postgre_missing_no_database, 
            user=jimBotSecrets.postgre_missing_no_user, 
            password=jimBotSecrets.postgre_missing_no_password, 
            port=jimBotSecrets.postgre_missing_no_port)

    def commit_transaction(self):
        if self._connection:
            self._connection.commit()
            self._connection.close()
            self._connection = None

    def rollback_transaction(self):
        if self._connection:
            self._connection.rollback()
            self._connection.close()
            self._connection = None


    def create_trainer(self, trainer: Trainer):
        with self._connection.cursor() as cursor:
            if len(trainer.created_by.strip()) == 0:
                raise Exception(f"created_by is required to insert a Trainer.")
            
            cursor.execute(f"""
                INSERT INTO Trainer (discord_name, name, is_active, created_by)
                VALUES ('{trainer.discord_name}', '{trainer.name}', {trainer.is_active}, '{trainer.created_by}')
                ;"""
            )

            if cursor.rowcount != 1:
                raise Exception(f"insert rowcount of Trainer {trainer.discord_name} return {cursor.rowcount}.")

    def read_trainers(self, trainer: Trainer = None) -> list[Trainer]:
        trainers = []

        with self._connection.cursor() as cursor:
            search_discord_name = ""
            search_name = ""
            search_is_active = ""

            if trainer is not None:
                if len(trainer.discord_name.strip()) > 0:
                    search_discord_name = f"  AND discord_name = '{trainer.discord_name}'"
                if len(trainer.name.strip()) > 0:
                    search_name = f"  AND name = '{trainer.name}'"
                if trainer.is_active == True:
                    search_is_active = f"  AND is_active = True"

            cursor.execute(f"""
                SELECT
                    discord_name,
                    name,
                    is_active
                FROM Trainer
                WHERE 1=1
                {search_discord_name}
                {search_name}
                {search_is_active}
                ORDER BY created_at ASC
                ;"""
            )

            for row in cursor.fetchall():
                trainers.append(Trainer(discord_name=row[0], name=row[1], is_active=row[2]))
            
        return trainers

    def update_trainer(self, trainer: Trainer):
        with self._connection.cursor() as cursor:
            cursor.execute(f"""
                UPDATE Trainer
                SET name = '{trainer.name}', is_active = {trainer.is_active}
                WHERE 1=1
                    AND discord_name = '{trainer.discord_name}'
                ;"""
            )

            if cursor.rowcount != 1:
                raise Exception(f"update rowcount of Trainer {trainer.discord_name} return {cursor.rowcount}.")

    def delete_trainer(self, trainer: Trainer):
        with self._connection.cursor() as cursor:
            cursor.execute(f"""
                DELETE FROM Trainer 
                WHERE 1=1
                    AND discord_name = '{trainer.discord_name}'
                ;"""
            )

            if cursor.rowcount != 1:
                raise Exception(f"delete rowcount of Trainer {trainer.discord_name} return {cursor.rowcount}.")


    def create_season(self, season: Season):
        with self._connection.cursor() as cursor:
            if len(season.created_by.strip()) == 0:
                raise Exception(f"created_by is required to insert a Season.")
            
            cursor.execute(f"""
                INSERT INTO Season (name, badge_points, is_active, created_by)
                VALUES ('{season.name}', {season.badge_points}, {season.is_active}, '{season.created_by}')
                ;"""
            )

            if cursor.rowcount != 1:
                raise Exception(f"insert rowcount of Season {season.name} return {cursor.rowcount}.")

    def read_seasons(self, season: Season) -> list[Season]:
        seasons = []

        with self._connection.cursor() as cursor:
            search_name = ""
            search_badge_points = ""
            search_is_active = ""

            if season is not None:
                if len(season.name.strip()) > 0:
                    search_name = f"  AND name = '{season.name}'"
                if season.badge_points > 0:
                    search_badge_points = f"  AND badge_points = {season.badge_points}"
                if season.is_active == True:
                    search_is_active = f"  AND is_active = True"

            cursor.execute(f"""
                SELECT
                    name,
                    badge_points,
                    is_active
                FROM Season
                WHERE 1=1
                {search_name}
                {search_badge_points}
                {search_is_active}
                ORDER BY created_at ASC
                ;"""
            )

            for row in cursor.fetchall():
                seasons.append(Season(name=row[0], badge_points=row[1], is_active=row[2]))
            
        return seasons

    def update_season(self, season: Season):
        with self._connection.cursor() as cursor:
            cursor.execute(f"""
                UPDATE Season
                SET badge_points = {season.badge_points}, is_active = {season.is_active}
                WHERE 1=1
                    AND name = '{season.name}'
                ;"""
            )

            if cursor.rowcount != 1:
                raise Exception(f"update rowcount of Season {season.name} return {cursor.rowcount}.")

    def delete_season(self, season: Season):
        with self._connection.cursor() as cursor:
            cursor.execute(f"""
                DELETE FROM Season
                WHERE 1=1
                    AND name = '{season.name}'
                ;"""
            )

            if cursor.rowcount != 1:
                raise Exception(f"delete rowcount of Season {season.name} return {cursor.rowcount}.")


    def create_scoreboard(self, scoreboard: Scoreboard):
        with self._connection.cursor() as cursor:
            if len(scoreboard.created_by.strip()) == 0:
                raise Exception(f"created_by is required to insert a Scoreboard.")
            
            cursor.execute(f"""
                INSERT INTO Scoreboard (season_name, trainer_discord_name, action_name, created_by)
                VALUES ('{scoreboard.season_name}', '{scoreboard.trainer_discord_name}', '{scoreboard.action.name}', '{scoreboard.created_by}')
                ;"""
            )

            if cursor.rowcount != 1:
                raise Exception(f"insert rowcount of Scoreboard {scoreboard.season_name}, {scoreboard.trainer_discord_name} return {cursor.rowcount}.")

    def read_scoreboards(self, scoreboard: Scoreboard) -> list[Scoreboard]:
        scoreboards = []

        with self._connection.cursor() as cursor:
            search_season_name = ""
            search_trainer_discord_name = ""
            search_actions = ""

            if scoreboard is not None:
                if len(scoreboard.season_name.strip()) > 0:
                    search_season_name = f"  AND Scoreboard.season_name = '{scoreboard.season_name}'"
                if len(scoreboard.trainer_discord_name.strip()) > 0:
                    search_trainer_discord_name = f"  AND Scoreboard.trainer_discord_name = '{scoreboard.trainer_discord_name}'"
                if scoreboard.action != ScoreboardAction.NONE:
                    search_actions = f"  AND Action.name = '{scoreboard.action}'"

            cursor.execute(f"""
                SELECT
                    Scoreboard.season_name,
                    Scoreboard.trainer_discord_name,
                    Action.name,
                    Action.points
                FROM Scoreboard
                    INNER JOIN Action ON Scoreboard.action_name = Action.name
                WHERE 1=1
                {search_season_name}
                {search_trainer_discord_name}
                {search_actions}
                ORDER BY Scoreboard.created_at ASC
                ;"""
            )

            for row in cursor.fetchall():
                scoreboards.append(Scoreboard(season_name=row[0], trainer_discord_name=row[1], action=row[2], points=row[3]))
            
        return scoreboards

    def delete_scoreboard(self, scoreboard: Scoreboard):
        with self._connection.cursor() as cursor:
            cursor.execute(f"""
                DELETE FROM Scoreboard
                WHERE 1=1
                    AND season_name = '{scoreboard.season_name}'
                    AND trainer_discord_name = '{scoreboard.trainer_discord_name}'
                    AND action_name = '{scoreboard.action.name}'
                    AND created_at = (
                        SELECT MAX(created_at) 
                        FROM Scoreboard 
                        WHERE 1=1
                            AND season_name = '{scoreboard.season_name}' 
                            AND trainer_discord_name = '{scoreboard.trainer_discord_name}'
                            AND action_name = '{scoreboard.action.name}'
                    )
                ;"""
            )

            if cursor.rowcount != 1:
                raise Exception(f"delete rowcount of Scoreboard {scoreboard.season_name}, {scoreboard.trainer_discord_name} return {cursor.rowcount}.")