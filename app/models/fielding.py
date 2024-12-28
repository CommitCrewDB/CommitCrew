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


class Fielding:
    def __init__(self, ID, playerID, yearID, stint, teamID, team_ID, lgID, POS, G, GS, InnOuts, PO, A, E, DP, PB, WP, SB, CS, ZR):
        self.ID = ID
        self.playerID = playerID
        self.yearID = yearID
        self.stint = stint
        self.teamID = teamID
        self.team_ID = team_ID
        self.lgID = lgID
        self.POS = POS
        self.G = G
        self.GS = GS
        self.InnOuts = InnOuts
        self.PO = PO
        self.A = A
        self.E = E
        self.DP = DP
        self.PB = PB
        self.WP = WP
        self.SB = SB
        self.CS = CS
        self.ZR = ZR

    @staticmethod
    def get_all_fielding():
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor() 

            query = """
                SELECT 
                    playerID, yearID, stint, teamID, lgID, POS, G, GS, InnOuts, 
                    PO, A, E, DP, PB, WP, SB, CS, ZR
                FROM fielding
            """
            cursor.execute(query)
            fielding_records = cursor.fetchall()

            cursor.close()
            connection.close()
            return fielding_records
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    @staticmethod
    def search_by_position(position):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor() 

            query = """
                SELECT 
                    playerID, yearID, stint, teamID, lgID, POS, G, GS, InnOuts, 
                    PO, A, E, DP, PB, WP, SB, CS, ZR
                FROM fielding
                WHERE POS LIKE %s
            """
            cursor.execute(query, (f"%{position}%",))
            fielding_records = cursor.fetchall()

            cursor.close()
            connection.close()
            return fielding_records
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
            
    @staticmethod
    def filter_fielding(player_id=None, year=None, position=None, leagues=None, ):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT playerID, yearID, teamID, lgID, POS, G, PO, A, E
                FROM fielding
                WHERE 1=1
            """
            params = []
            if leagues:
                query += " AND lgID IN ({})".format(",".join(["%s"] * len(leagues)))
                params.extend(leagues)
            if player_id:
                query += " AND playerID LIKE %s"
                params.append(f"%{player_id}%")
            if year:
                query += " AND yearID = %s"
                params.append(year)
            if position:
                query += " AND POS = %s"
                params.append(position)

            cursor.execute(query, params)
            results = cursor.fetchall()

            cursor.close()
            connection.close()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    @staticmethod
    def get_all_leagues():
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()  

            query = "SELECT lgID, league FROM leagues"
            cursor.execute(query)
            leagues = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

            cursor.close()
            connection.close()
            return leagues
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
