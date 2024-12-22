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
                SELECT t1.yearID, t1.lgID, l.league AS league_name, t1.name AS team_name, t1.W AS wins
                FROM teams t1
                INNER JOIN (
                    SELECT lgID, MAX(W) AS MaxWins
                    FROM teams
                    WHERE lgID IS NOT NULL AND W IS NOT NULL
                    GROUP BY lgID
                ) t2 ON t1.lgID = t2.lgID AND t1.W = t2.MaxWins
                INNER JOIN leagues l ON t1.lgID = l.lgID
            """
            cursor.execute(query)

            # Collecting result as a list of dictionaries for rendering
            top_league_teams = [{"Year": row[0], "LeagueID": row[1], "LeagueName": row[2], "Team": row[3], "Wins": row[4]} for row in cursor.fetchall()]

            cursor.close()
            db.close()
            return top_league_teams
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        
    @staticmethod
    def get_top_teams_by_year():
        try:
            db = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME", "lahmansbaseballdb")
            )
            cursor = db.cursor()

            query = """
                SELECT t1.yearID, t1.lgID, l.league AS league_name, t1.name AS team_name, t1.W AS wins
                FROM teams t1
                INNER JOIN (
                    SELECT yearID, MAX(W) as MaxWins
                    FROM teams
                    WHERE yearID IS NOT NULL AND W IS NOT NULL
                    GROUP BY yearID
                ) t2
                ON t1.yearID = t2.yearID AND t1.W = t2.MaxWins
                INNER JOIN leagues l ON t1.lgID = l.lgID
            """
            cursor.execute(query)

            # Collecting result as a list of dictionaries for rendering
            top_year_teams = [{"Year": row[0], "LeagueID": row[1], "LeagueName": row[2], "Team": row[3], "Wins": row[4]} for row in cursor.fetchall()]

            cursor.close()
            db.close()
            return top_year_teams
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []


    @staticmethod
    def add_team(team_data):
        try:
            db = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            cursor = db.cursor()
            query = """
                INSERT INTO teams (yearID, lgID, name, franchID, W, L)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (team_data["Year"], team_data["League"], team_data["Team"],
                                team_data["Franchise"], team_data["Wins"], team_data["Losses"]))
            db.commit()
            cursor.close()
            db.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    @staticmethod
    def delete_team(team_id):
        try:
            db = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            cursor = db.cursor()
            query = "DELETE FROM teams WHERE teamID = %s"
            cursor.execute(query, (team_id,))
            db.commit()
            cursor.close()
            db.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False


