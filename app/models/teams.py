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

class Teams:
    def __init__(self, Year, League, TeamID, Team, Franchise, TeamDivision, Rank, GamesPlayed, HomeGames, Wins, Losses):
        self.Year = Year
        self.League = League
        self.TeamID = TeamID
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
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()  

            query = """
                SELECT 
                    yearID, lgID, teamID, name, franchID, divID, teamRank, G, Ghome, W, L 
                FROM teams
            """
            cursor.execute(query)
            teams = []
            for row in cursor.fetchall():
                teams.append(Teams(*row))

            cursor.close()
            connection.close()
            return teams
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    @staticmethod
    def search_by_name(team_name):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()  

            query = """
                SELECT yearID, lgID, teamID, name, franchID, divID, teamRank, G, Ghome, W, L 
                FROM teams
                WHERE name LIKE %s
            """
            cursor.execute(query, (f"%{team_name}%",))
            teams = [Teams(*row) for row in cursor.fetchall()]

            cursor.close()
            connection.close()
            return teams
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    @staticmethod
    def get_top_teams_by_league():
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()  

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
            connection.close()
            return top_league_teams
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        
    @staticmethod
    def get_top_teams_by_year():
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()  

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
            connection.close()
            return top_year_teams
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []


    @staticmethod
    def add_team(team_data):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()
            query = """
                INSERT INTO teams (yearID, lgID, name, franchID, W, L, teamID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                team_data["yearID"],
                team_data["League"],
                team_data["Team"],
                team_data["Franchise"],
                team_data["Wins"],
                team_data["Losses"],
                team_data["TeamID"]
            ))
            connection.commit()
            print("Team added successfully.")
        except mysql.connector.Error as err:
            print(f"SQL Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def delete_team(team_id):
        connection = create_connection()
        if connection is None:
            print("Database connection failed.")
            return

        try:
            cursor = connection.cursor()
            query = "DELETE FROM teams WHERE teamID = %s"
            cursor.execute(query, (team_id,))
            connection.commit()
            print(f"Team with teamID {team_id} deleted successfully.")
        except mysql.connector.Error as err:
            print(f"SQL Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    @staticmethod
    def filter_teams(leagues=None, year=None, team_name=None, sort_by=None):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()

            query = """
                SELECT yearID, lgID, teamID, name, franchID, divID, teamRank, G, Ghome, W, L
                FROM teams
                WHERE 1=1
            """
            params = []

            if leagues:
                query += " AND lgID IN ({})".format(",".join(["%s"] * len(leagues)))
                params.extend(leagues)

            if year:
                query += " AND yearID = %s"
                params.append(year)

            if team_name:
                query += " AND name LIKE %s"
                params.append(f"%{team_name}%")

            if sort_by == "wins_asc":
                query += " ORDER BY W ASC"
            elif sort_by == "wins_desc":
                query += " ORDER BY W DESC"
            elif sort_by == "year_asc":
                query += " ORDER BY yearID ASC"
            elif sort_by == "year_desc":
                query += " ORDER BY yearID DESC"
            elif sort_by == "team_name_asc":
                query += " ORDER BY name ASC"
            elif sort_by == "team_name_desc":
                query += " ORDER BY name DESC"
            elif sort_by == "rank_asc":
                query += " ORDER BY teamRank ASC"
            elif sort_by == "rank_desc":
                query += " ORDER BY teamRank DESC"

            cursor.execute(query, tuple(params))
            teams = [Teams(*row) for row in cursor.fetchall()]

            cursor.close()
            connection.close()
            return teams
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
        
    @staticmethod
    def update_team(team_id, updated_data):
        connection = create_connection()
        if connection is None:
            raise Exception("Database connection failed.")
        cursor = connection.cursor()
        query = """
            UPDATE teams
            SET name = %s, teamRank = %s, divID = %s, G = %s, W = %s, L = %s
            WHERE teamID = %s
        """
        params = (
            updated_data["Team"],
            updated_data["Rank"],
            updated_data["TeamDivision"],
            updated_data["GamesPlayed"],
            updated_data["Wins"],
            updated_data["Losses"],
            team_id,
        )
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_team_by_id(team_id):
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM teams WHERE TeamID = %s"
        try:
            cursor.execute(query, (team_id,))
            team = cursor.fetchone() 
            return team
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            while cursor.nextset():
                pass
            cursor.close()
            connection.close()

                

    


