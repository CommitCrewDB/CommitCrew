import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
            db = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME", "lahmansbaseballdb")
            )
            cursor = db.cursor()

            query = """
                SELECT 
                    ID, playerID, yearID, stint, teamID, team_ID, lgID, POS, G, GS, InnOuts, 
                    PO, A, E, DP, PB, WP, SB, CS, ZR
                FROM fielding
            """
            cursor.execute(query)
            fielding_records = []
            for row in cursor.fetchall():
                fielding_records.append(Fielding(*row))

            cursor.close()
            db.close()
            return fielding_records
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    
    def search_by_position(position):
        try:
            db = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME", "lahmansbaseballdb")
            )
            cursor = db.cursor()

            query = """
                SELECT 
                    ID, playerID, yearID, stint, teamID, team_ID, lgID, POS, G, GS, InnOuts, 
                    PO, A, E, DP, PB, WP, SB, CS, ZR
                FROM fielding
                WHERE POS LIKE %s
            """
            cursor.execute(query, (f"%{position}%",))
            fielding_records = [Fielding(*row) for row in cursor.fetchall()]

            cursor.close()
            db.close()
            return fielding_records
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

