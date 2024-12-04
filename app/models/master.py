import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Database:
    @staticmethod
    def get_connection():
        """Establish and return a database connection."""
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "lahmansbaseballdb")
        )


class Master:
    def __init__(self, playerID, birthYear, birthMonth, birthDay, birthCountry, birthState, birthCity, 
                 deathYear, deathMonth, deathDay, deathCountry, deathState, deathCity, nameFirst, 
                 nameLast, nameGiven, weight, height, bats, throws, debut, finalGame, retroID, bbrefID):
        self.playerID = playerID
        self.birthYear = birthYear
        self.birthMonth = birthMonth
        self.birthDay = birthDay
        self.birthCountry = birthCountry
        self.birthState = birthState
        self.birthCity = birthCity
        self.deathYear = deathYear
        self.deathMonth = deathMonth
        self.deathDay = deathDay
        self.deathCountry = deathCountry
        self.deathState = deathState
        self.deathCity = deathCity
        self.nameFirst = nameFirst
        self.nameLast = nameLast
        self.nameGiven = nameGiven
        self.weight = weight
        self.height = height
        self.bats = bats
        self.throws = throws
        self.debut = debut
        self.finalGame = finalGame
        self.retroID = retroID
        self.bbrefID = bbrefID

    @staticmethod
    def get_all_records():
        """Retrieve all records from the master table."""
        try:
            db = Database.get_connection()
            cursor = db.cursor()

            query = """
                SELECT 
                    playerID, birthYear, birthMonth, birthDay, birthCountry, birthState, birthCity, 
                    deathYear, deathMonth, deathDay, deathCountry, deathState, deathCity, nameFirst, 
                    nameLast, nameGiven, weight, height, bats, throws, debut, finalGame, retroID, bbrefID
                FROM master
            """
            cursor.execute(query)
            master_records = [Master(*row) for row in cursor.fetchall()]

            cursor.close()
            db.close()
            return master_records
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    @staticmethod
    def get_record_by_id(playerID):
        """Retrieve a specific record by playerID."""
        try:
            db = Database.get_connection()
            cursor = db.cursor()

            query = """
                SELECT 
                    playerID, birthYear, birthMonth, birthDay, birthCountry, birthState, birthCity, 
                    deathYear, deathMonth, deathDay, deathCountry, deathState, deathCity, nameFirst, 
                    nameLast, nameGiven, weight, height, bats, throws, debut, finalGame, retroID, bbrefID
                FROM master
                WHERE playerID = %s
            """
            cursor.execute(query, (playerID,))
            record = cursor.fetchone()

            cursor.close()
            db.close()
            return Master(*record) if record else None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
