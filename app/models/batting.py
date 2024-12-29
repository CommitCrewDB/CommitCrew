import mysql.connector
from app.db_init import get_db

class Batting:
    @staticmethod
    def get_paginated_batting(offset, limit):
        """
        Fetch paginated batting records.
        """
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                batting.*, 
                master.nameFirst, 
                master.nameLast 
            FROM batting 
            LEFT JOIN master ON batting.playerID = master.playerID
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, offset))
        return cursor.fetchall()

    @staticmethod
    def get_total_batting_records():
        """
        Get the total count of batting records.
        """
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT COUNT(*) AS total FROM batting"
        cursor.execute(query)
        result = cursor.fetchone()
        return result["total"]

    @staticmethod
    def get_all_batting():
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                batting.*, 
                master.nameFirst, 
                master.nameLast 
            FROM batting 
            LEFT JOIN master ON batting.playerID = master.playerID
        """
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def search_batting(year=None, team=None, leagues=None, sort_by=None, sort_order="asc"):
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                batting.*, 
                master.nameFirst, 
                master.nameLast 
            FROM batting 
            LEFT JOIN master ON batting.playerID = master.playerID
            WHERE 1=1
        """
        params = []

        if year:
            query += " AND batting.yearID = %s"
            params.append(year)
        if team:
            query += " AND batting.teamID = %s"
            params.append(team)
        if leagues:
            query += " AND batting.lgID IN (%s)" % ', '.join(['%s'] * len(leagues))
            params.extend(leagues)

        if sort_by:
            query += f" ORDER BY {sort_by} {sort_order.upper()}"

        cursor.execute(query, tuple(params))
        return cursor.fetchall()

    @staticmethod
    def get_leagues():
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT lgID, league, active FROM leagues"
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_by_id(record_id):
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                batting.*, 
                master.nameFirst, 
                master.nameLast 
            FROM batting 
            LEFT JOIN master ON batting.playerID = master.playerID
            WHERE batting.ID = %s
        """
        cursor.execute(query, (record_id,))
        return cursor.fetchone()

    def insert(player_id, year_id, stint, team_id, lg_id, **kwargs):
        """
        Insert a new batting record.
        :param player_id: Player ID (string).
        :param year_id: Year ID (integer).
        :param stint: Stint (integer).
        :param team_id: Team ID (string).
        :param lg_id: League ID (string).
        :param kwargs: Other batting stats (e.g., G, AB, HR, etc.).
        """
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        columns = ['playerID', 'yearID', 'stint', 'teamID', 'lgID']
        values = [player_id, year_id, stint, team_id, lg_id]
        for key, value in kwargs.items():
            columns.append(key)
            values.append(value)
        query = f"INSERT INTO batting ({','.join(columns)}) VALUES ({','.join(['%s'] * len(values))})"
        cursor.execute(query, tuple(values))
        connection.commit()

    def update(record_id, **kwargs):
        """
        Update an existing batting record.
        :param record_id: ID of the record to update.
        :param kwargs: Key-value pairs of columns to update.
        """
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        updates = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE batting SET {updates} WHERE ID = %s"
        cursor.execute(query, tuple(kwargs.values()) + (record_id,))
        connection.commit()

    def delete(record_id):
        """
        Delete a batting record by ID.
        :param record_id: ID of the record to delete.
        """
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = "DELETE FROM batting WHERE ID = %s"
        cursor.execute(query, (record_id,))
        connection.commit()
