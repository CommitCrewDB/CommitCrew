import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Teams:
    def __init__(self, Year, League, Team, Franchise, TeamDivision, Rank, GamesPlayed, HomeGames, Wins, Losses):
        self.Year = Year
        self.League = League
        self.Team = Team
        self.Franchise = Franchise
        self.TeamDivision = TeamDivision
        self.Rank = Rank
        self.GamesPlayed = GamesPlayed
        self.HomeGames = HomeGames
        self.Wins = Wins
        self.Losses = Losses

    @staticmethod
    def get_all_teams():
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
                    yearID, lgID, name, franchID, divID, teamRank, G, Ghome, W, L 
                FROM teams
            """
            cursor.execute(query)
            teams = []
            for row in cursor.fetchall():
                teams.append(Teams(*row))

            cursor.close()
            db.close()
            return teams
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []