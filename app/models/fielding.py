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
    def __init__(self, ID, playerID, yearID, stint, teamID, lgID, POS, G, GS, InnOuts, PO, A, E, DP, PB, WP, SB, CS, ZR):
        self.ID = ID
        self.playerID = playerID
        self.yearID = yearID
        self.stint = stint
        self.teamID = teamID
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
        self.ZR = ZR or 0

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
                    PO, A, E, DP, PB, WP, SB
                FROM fielding
            """
            cursor.execute(query)
            fielding_records = []

            for row in cursor.fetchall():
                fielding_records.append(Fielding(*row))

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
                    PO, A, E, DP, PB, WP, SB
                FROM fielding
                WHERE POS LIKE %s
            """
            cursor.execute(query, (f"%{position}%",))
            fielding_records = [Fielding(*row) for row in cursor.fetchall()]

            cursor.close()
            connection.close()
            return fielding_records
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
            
    @staticmethod
    def filter_fielding(player_id=None, year=None, position=None, leagues=None):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return []
            cursor = connection.cursor()

            query = """
                SELECT ID, playerID, yearID, stint, teamID, lgID, POS, G, GS, InnOuts, PO, A, E, DP, PB, WP, SB, CS, ZR
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

            cursor.execute(query, tuple(params))
            results = [Fielding(*row) for row in cursor.fetchall()]

            cursor.close()
            connection.close()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []


    @staticmethod
    def add_fielding_record(fielding_data):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()

            # Check if the record already exists
            check_query = """
                SELECT 1 FROM fielding
                WHERE playerID = %s AND yearID = %s AND stint = %s AND teamID = %s
            """
            cursor.execute(check_query, (
                fielding_data["player_id"],
                fielding_data["year"],
                fielding_data["stint"],
                fielding_data["team_id"],
            ))
            if cursor.fetchone():
                raise ValueError("Duplicate record: Fielding record already exists.")

            # Insert new record
            query = """
                INSERT INTO fielding (
                    playerID, yearID, stint, teamID, lgID, POS, G, PO
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                fielding_data["player_id"],
                fielding_data["year"],
                fielding_data["stint"],
                fielding_data["team_id"],
                fielding_data["league"],
                fielding_data["position"],
                fielding_data["games"],
                fielding_data["po"],
            ))
            connection.commit()
            print("Fielding record added successfully.")
        except mysql.connector.IntegrityError as e:
            print(f"Integrity Error: {e}")
            raise e
        except ValueError as ve:
            print(f"Validation Error: {ve}")
            raise ve
        except mysql.connector.Error as err:
            print(f"SQL Error: {err}")
            raise err
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


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
    def get_record_by_id(record_id):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return None
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM fielding WHERE ID = %s"
            cursor.execute(query, (record_id,))
            record = cursor.fetchone()
            return record
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    @staticmethod
    def update_record(record_id, updated_data):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()
            query = """
                UPDATE fielding
                SET playerID = %s, yearID = %s, stint = %s, teamID = %s, lgID = %s, POS = %s, G = %s, PO = %s
                WHERE ID = %s
            """
            cursor.execute(query, (
                updated_data["playerID"],
                updated_data["yearID"],
                updated_data["stint"],
                updated_data["teamID"],
                updated_data["lgID"],
                updated_data["POS"],
                updated_data["G"],
                updated_data["PO"],
                record_id,
            ))
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def delete_record(record_id):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return
            cursor = connection.cursor()
            query = "DELETE FROM fielding WHERE ID = %s"
            cursor.execute(query, (record_id,))
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    @staticmethod
    def get_top_fielding_players(year):
        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed.")
                return []
            
            query = """
                SELECT 
                    f.playerID, 
                    m.nameFirst, 
                    m.nameLast, 
                    f.yearID, 
                    f.lgID, 
                    f.POS, 
                    SUM(f.PO) AS total_putouts, 
                    SUM(f.A) AS total_assists, 
                    SUM(f.G) AS games_played
                FROM 
                    fielding AS f
                JOIN 
                    master AS m ON f.playerID = m.playerID
                WHERE 
                    f.yearID = %s
                GROUP BY 
                    f.POS, f.playerID, f.lgID
                ORDER BY 
                    total_putouts DESC, total_assists DESC
            """
            
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (year,))
                results = cursor.fetchall()
            
            connection.close()
            return results

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
