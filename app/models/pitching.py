import os
import mysql.connector
from dotenv import load_dotenv
from flask import jsonify

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

class Pitching:
    def __init__(self, playerID, yearID, stint, teamID, lgID, W, L, ERA, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, SO, BAOpp):
        self.playerID = playerID
        self.yearID = yearID
        self.stint = stint
        self.teamID = teamID
        self.lgID = lgID
        self.W = W
        self.L = L
        self.ERA = ERA
        self.G = G
        self.GS = GS
        self.CG = CG
        self.SHO = SHO
        self.SV = SV
        self.IPouts = IPouts
        self.H = H
        self.ER = ER
        self.HR = HR
        self.BB = BB
        self.SO = SO
        self.BAOpp = BAOpp

    @staticmethod
    def get_all_pitching(sort_by='yearID', order='ASC', limit=10, offset=0):
        connection = create_connection()
        if not connection:
            return [], 0

        query = f"""
            SELECT id, playerID, yearID, stint, teamID, lgID, W, L, ERA, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, SO, BAOpp
            FROM pitching
            ORDER BY {sort_by} {order}
            LIMIT {limit} OFFSET {offset}
        """

        count_query = "SELECT COUNT(*) AS total FROM pitching"

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()

            cursor.execute(count_query)
            total_records = cursor.fetchone()['total']

            return data, total_records
        except Exception as e:
            print(f"Error fetching pitching data: {e}")
            return [], 0
        finally:
            connection.close()

    @staticmethod
    def add_pitching(data):
        connection = create_connection()
        if not connection:
            return False

        query = """
        INSERT INTO pitching (playerID, yearID, stint, teamID, lgID, W, L, ERA, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, SO, BAOpp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

        """
        try:
            cursor = connection.cursor()
            cursor.execute(query, (
                data['playerID'],
                data['yearID'],
                data['stint'],
                data['teamID'],
                data['lgID'],
                data['W'],
                data['L'],
                data['ERA'],
                data['G'],
                data['GS'],
                data['CG'],
                data['SHO'],
                data['SV'],
                data['IPouts'],
                data['H'],
                data['ER'],
                data['HR'],
                data['BB'],
                data['SO'],
                data['BAOpp']
            ))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error adding pitching data: {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def delete_pitching_by_id(record_id):
        connection = create_connection()
        if not connection:
            return False

        query = "DELETE FROM pitching WHERE id = %s"

        try:
            cursor = connection.cursor()
            cursor.execute(query, (record_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting pitching data: {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def update_pitching(record_id, updated_data):
        connection = create_connection()
        if connection is None:
            raise Exception("Database connection failed.")

        query = """
            UPDATE pitching
            SET 
                playerID = %s,
                yearID = %s,
                stint = %s,
                teamID = %s,
                lgID = %s,
                W = %s,
                L = %s,
                ERA = %s,
                G = %s,
                GS = %s,
                CG = %s,
                SHO = %s,
                SV = %s,
                IPouts = %s,
                H = %s,
                ER = %s,
                HR = %s,
                BB = %s,
                SO = %s,
                BAOpp = %s
            WHERE id = %s
        """
        params = (
            updated_data.get("playerID"),
            updated_data.get("yearID"),
            updated_data.get("stint"),
            updated_data.get("teamID"),
            updated_data.get("lgID"),
            updated_data.get("W"),
            updated_data.get("L"),
            updated_data.get("ERA"),
            updated_data.get("G"),
            updated_data.get("GS"),
            updated_data.get("CG"),
            updated_data.get("SHO"),
            updated_data.get("SV"),
            updated_data.get("IPouts"),
            updated_data.get("H"),
            updated_data.get("ER"),
            updated_data.get("HR"),
            updated_data.get("BB"),
            updated_data.get("SO"),
            updated_data.get("BAOpp"),
            record_id,
        )

        try:
            cursor = connection.cursor()
            print(f"Executing query: {query}")  # Debugging
            print(f"With parameters: {params}")  # Debugging
            cursor.execute(query, params)
            connection.commit()
            print(f"Record with ID {record_id} updated successfully.")  # Debugging
            return True
        except Exception as e:
            print(f"Error occurred while updating record {record_id}: {e}")  # Debugging
            return False
        finally:
            connection.close()
