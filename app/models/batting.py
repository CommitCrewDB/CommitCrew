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
                master.nameLast, 
                teams.name AS teamName 
            FROM batting 
            LEFT JOIN master ON batting.playerID = master.playerID
            LEFT JOIN teams ON batting.teamID = teams.teamID
                AND batting.yearID = teams.yearID
                AND batting.lgID = teams.lgID
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
                master.nameLast, 
                teams.name AS teamName 
            FROM batting 
            LEFT JOIN master ON batting.playerID = master.playerID
            LEFT JOIN teams ON batting.teamID = teams.teamID
                AND batting.yearID = teams.yearID
                AND batting.lgID = teams.lgID
        """
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_batting_average_by_year():
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = """
            WITH BattingWithAverage AS (
                SELECT 
                    CONCAT(m.nameFirst, ' ', m.nameLast) AS playerName,
                    b.playerID,
                    b.yearID,
                    b.teamID,
                    t.name AS teamName,
                    b.lgID,
                    b.stint,
                    b.AB,
                    b.H,
                    CASE 
                        WHEN b.AB > 0 THEN CAST(b.H AS FLOAT) / b.AB 
                        ELSE 0 
                    END AS battingAverage
                FROM batting b
                LEFT JOIN master m ON b.playerID = m.playerID
                LEFT JOIN teams t ON b.teamID = t.teamID AND b.yearID = t.yearID AND b.lgID = t.lgID
            ),
            YearlyStats AS (
                SELECT 
                    yearID,
                    MAX(battingAverage) AS maxBattingAverage,
                    AVG(battingAverage) AS avgBattingAverage
                FROM BattingWithAverage
                GROUP BY yearID
            )
            SELECT 
                b.playerName,
                b.playerID,
                b.yearID,
                b.teamID,
                b.teamName,
                b.lgID,
                b.stint,
                b.AB,
                b.H,
                b.battingAverage,
                y.avgBattingAverage
            FROM BattingWithAverage b
            JOIN YearlyStats y
                ON b.yearID = y.yearID AND b.battingAverage = y.maxBattingAverage
            ORDER BY b.yearID DESC;
        """
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_batting_average_by_team():
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = """
            WITH BattingWithAverage AS (
                SELECT 
                    CONCAT(m.nameFirst, ' ', m.nameLast) AS playerName,
                    b.playerID,
                    b.yearID,
                    b.teamID,
                    t.name AS teamName,
                    b.lgID,
                    b.stint,
                    b.AB,
                    b.H,
                    CASE 
                        WHEN b.AB > 0 THEN CAST(b.H AS FLOAT) / b.AB 
                        ELSE 0 
                    END AS battingAverage
                FROM batting b
                LEFT JOIN master m ON b.playerID = m.playerID
                LEFT JOIN teams t ON b.teamID = t.teamID AND b.yearID = t.yearID AND b.lgID = t.lgID
            ),
            TeamStats AS (
                SELECT 
                    teamID,
                    MAX(battingAverage) AS maxBattingAverage,
                    AVG(battingAverage) AS avgBattingAverage
                FROM BattingWithAverage
                GROUP BY teamID
            )
            SELECT 
                b.playerName,
                b.playerID,
                b.yearID,
                b.teamID,
                b.teamName,
                b.lgID,
                b.stint,
                b.AB,
                b.H,
                b.battingAverage,
                t.avgBattingAverage
            FROM BattingWithAverage b
            JOIN TeamStats t
                ON b.teamID = t.teamID AND b.battingAverage = t.maxBattingAverage
            ORDER BY b.teamID;
        """
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_batting_average_by_league():
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = """
            WITH BattingWithAverage AS (
                SELECT 
                    CONCAT(m.nameFirst, ' ', m.nameLast) AS playerName,
                    b.playerID,
                    b.yearID,
                    b.teamID,
                    t.name AS teamName,
                    b.lgID,
                    b.stint,
                    b.AB,
                    b.H,
                    CASE 
                        WHEN b.AB > 0 THEN CAST(b.H AS FLOAT) / b.AB 
                        ELSE 0 
                    END AS battingAverage
                FROM batting b
                LEFT JOIN master m ON b.playerID = m.playerID
                LEFT JOIN teams t ON b.teamID = t.teamID AND b.yearID = t.yearID AND b.lgID = t.lgID
            ),
            LeagueStats AS (
                SELECT 
                    lgID,
                    MAX(battingAverage) AS maxBattingAverage,
                    AVG(battingAverage) AS avgBattingAverage
                FROM BattingWithAverage
                GROUP BY lgID
            )
            SELECT 
                b.playerName,
                b.playerID,
                b.yearID,
                b.teamID,
                b.teamName,
                b.lgID,
                b.stint,
                b.AB,
                b.H,
                b.battingAverage,
                l.avgBattingAverage
            FROM BattingWithAverage b
            JOIN LeagueStats l
                ON b.lgID = l.lgID AND b.battingAverage = l.maxBattingAverage
            ORDER BY b.lgID;
        """
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def search_batting(year=None, team=None, leagues=None, player=None, sort_by=None, sort_order="asc"):
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                batting.*, 
                master.nameFirst, 
                master.nameLast, 
                teams.name AS teamName 
            FROM batting 
            LEFT JOIN master ON batting.playerID = master.playerID
            LEFT JOIN teams ON batting.teamID = teams.teamID
                AND batting.yearID = teams.yearID
                AND batting.lgID = teams.lgID
            WHERE 1=1
        """
        params = []

        if year:
            query += " AND batting.yearID = %s"
            params.append(year)
        if team:
            query += " AND (batting.teamID = %s OR teams.name LIKE %s)"
            params.extend([team, f"%{team}%"])
        if leagues:
            query += " AND batting.lgID IN (%s)" % ', '.join(['%s'] * len(leagues))
            params.extend(leagues)
        if player:
            query += """
                AND (
                    master.playerID = %s OR 
                    master.nameFirst LIKE %s OR 
                    master.nameLast LIKE %s OR 
                    CONCAT(master.nameFirst, ' ', master.nameLast) LIKE %s
                )
            """
            params.extend([player, f"%{player}%", f"%{player}%", f"%{player}%"])
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
