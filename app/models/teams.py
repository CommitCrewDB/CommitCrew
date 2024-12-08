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

    @staticmethod
    def search_by_name(team_name):
        try:
            db = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME", "lahmansbaseballdb")
            )
            cursor = db.cursor()

            query = """
                SELECT yearID, lgID, name, franchID, divID, teamRank, G, Ghome, W, L 
                FROM teams
                WHERE name LIKE %s
            """
            cursor.execute(query, (f"%{team_name}%",))
            teams = [Teams(*row) for row in cursor.fetchall()]

            cursor.close()
            db.close()
            return teams
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    @staticmethod
    def get_top_teams_by_league():
        try:
            db = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME", "lahmansbaseballdb")
            )
            cursor = db.cursor()

            query = """
                SELECT t1.lgID, t1.name, t1.W
                FROM teams t1
                INNER JOIN (
                    SELECT lgID, MAX(W) as MaxWins
                    FROM teams
                    WHERE lgID IS NOT NULL AND W IS NOT NULL
                    GROUP BY lgID
                ) t2
                ON t1.lgID = t2.lgID AND t1.W = t2.MaxWins
            """
            cursor.execute(query)

            # Collecting result as a list of dictionaries for rendering
            top_teams = [{"League": row[0], "Team": row[1], "Wins": row[2]} for row in cursor.fetchall()]

            cursor.close()
            db.close()
            return top_teams
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []




