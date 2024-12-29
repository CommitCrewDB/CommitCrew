import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "lahmansbaseballdb"),
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

class Master:
    def __init__(self, ID, playerID, birthYear, birthMonth, birthDay, birthCity, birthCountry, birthState, deathYear, deathMonth, deathDay, deathCountry, deathState, deathCity, nameFirst, nameLast, nameGiven, weight, height, bats, throws, debut, bbrefID, finalGame, retroID):
        self.ID = ID
        self.playerID = playerID
        self.birthYear = birthYear
        self.birthMonth = birthMonth
        self.birthDay = birthDay
        self.birthCity = birthCity
        self.birthCountry = birthCountry
        self.birthState = birthState
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
        self.bbrefID = bbrefID
        self.finalGame = finalGame
        self.retroID = retroID

    @staticmethod
    def get_all_players():
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()

            query = """
                SELECT * FROM master
            """
            cursor.execute(query)
            players = [Master(*row) for row in cursor.fetchall()]

            cursor.close()
            connection.close()
            return players
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    @staticmethod
    def search_by_name(name):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()

            query = """
                SELECT * FROM master
                WHERE nameFirst LIKE %s OR nameLast LIKE %s
            """
            cursor.execute(query, (f"%{name}%", f"%{name}%"))
            players = [Master(*row) for row in cursor.fetchall()]

            cursor.close()
            connection.close()
            return players
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    @staticmethod
    def add_player(player_data):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()
            query = """
                INSERT INTO master (playerID, birthYear, birthMonth, birthDay, birthCity, birthCountry, birthState, deathYear, deathMonth, deathDay, deathCountry, deathState, deathCity, nameFirst, nameLast, nameGiven, weight, height, bats, throws, debut, bbrefID, finalGame, retroID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                player_data["playerID"], player_data["birthYear"], player_data["birthMonth"], player_data["birthDay"],
                player_data["birthCity"], player_data["birthCountry"], player_data["birthState"],
                player_data["deathYear"], player_data["deathMonth"], player_data["deathDay"],
                player_data["deathCountry"], player_data["deathState"], player_data["deathCity"],
                player_data["nameFirst"], player_data["nameLast"], player_data["nameGiven"],
                player_data["weight"], player_data["height"], player_data["bats"], player_data["throws"],
                player_data["debut"], player_data["bbrefID"], player_data["finalGame"], player_data["retroID"]
            ))
            connection.commit()
            print("Player added successfully.")
        except mysql.connector.Error as err:
            print(f"SQL Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def delete_player(player_id):
        connection = create_connection()
        if connection is None:
            print("Database connection failed.")
            return

        try:
            cursor = connection.cursor()
            query = "DELETE FROM master WHERE ID = %s"
            cursor.execute(query, (player_id,))
            connection.commit()
            print(f"Player with ID {player_id} deleted successfully.")
        except mysql.connector.Error as err:
            print(f"SQL Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def update_player(player_id, updated_data):
        connection = create_connection()
        if connection is None:
            raise Exception("Database connection failed.")
        cursor = connection.cursor()
        query = """
            UPDATE master
            SET nameFirst = %s, nameLast = %s, birthYear = %s, birthMonth = %s, birthDay = %s, weight = %s, height = %s
            WHERE ID = %s
        """
        params = (
            updated_data["nameFirst"], updated_data["nameLast"], updated_data["birthYear"],
            updated_data["birthMonth"], updated_data["birthDay"], updated_data["weight"],
            updated_data["height"], player_id
        )
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_player_by_id(player_id):
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM master WHERE ID = %s"
        try:
            cursor.execute(query, (player_id,))
            player = cursor.fetchone()
            return player
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
           
                connection.close()
    @staticmethod
    def filter_master(
        birth_country=None,
        birth_year=None,
        death_year=None,
        player_name=None,
        sort_by=None,
    ):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()

            query = """
                SELECT ID, playerID, birthYear, birthMonth, birthDay, birthCity, birthCountry, 
                       birthState, deathYear, deathMonth, deathDay, deathCountry, deathState, 
                       deathCity, nameFirst, nameLast, nameGiven, weight, height, bats, throws, 
                       debut, bbrefID, finalGame, retroID
                FROM master
                WHERE 1=1
            """
            params = []

            # Filtering by birth country
            if birth_country:
                query += " AND birthCountry = %s"
                params.append(birth_country)

            # Filtering by birth year
            if birth_year:
                query += " AND birthYear = %s"
                params.append(birth_year)

            # Filtering by death year
            if death_year:
                query += " AND deathYear = %s"
                params.append(death_year)

            # Filtering by player name (first or last)
            if player_name:
                query += " AND (nameFirst LIKE %s OR nameLast LIKE %s)"
                params.append(f"%{player_name}%")
                params.append(f"%{player_name}%")

            # Sorting options
            if sort_by == "birth_year_asc":
                query += " ORDER BY birthYear ASC"
            elif sort_by == "birth_year_desc":
                query += " ORDER BY birthYear DESC"
            elif sort_by == "death_year_asc":
                query += " ORDER BY deathYear ASC"
            elif sort_by == "death_year_desc":
                query += " ORDER BY deathYear DESC"
            elif sort_by == "player_name_asc":
                query += " ORDER BY nameFirst ASC, nameLast ASC"
            elif sort_by == "player_name_desc":
                query += " ORDER BY nameFirst DESC, nameLast DESC"

            cursor.execute(query, tuple(params))
            results = [Master(*row) for row in cursor.fetchall()]

            cursor.close()
            connection.close()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
