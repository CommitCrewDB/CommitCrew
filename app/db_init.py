import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
import click

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

path = r"<path/to/csv/"

def get_db(use_database=True):
    """
    Establish a connection to the MySQL server.

    :param use_database: If True, connect to the specific database; otherwise, connect to the server only.
    :return: A MySQL connection object.
    :raises RuntimeError: If the connection fails.
    """
    try:
        db = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""), # Ensure this is set in the .env file
                database=os.getenv("DB_NAME") if use_database else None,
                allow_local_infile=True
            )
        return db
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise RuntimeError("Database connection failed. Please check the configuration.")

def execute_query(connection, query, commit=False):
    """
    Execute a SQL query on the database.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        if commit:
            connection.commit()
    except Exception as e:
        print(f"Error executing query: {query}\n{e}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def create_database(connection):
    """
    Create the database schema.
    """
    execute_query(connection, "DROP DATABASE IF EXISTS lahmansbaseballdb;", commit=True)
    execute_query(connection, "CREATE DATABASE lahmansbaseballdb;", commit=True)
    execute_query(connection, "USE lahmansbaseballdb;")

def set_encoding(connection):
    """
    Set the database encoding to UTF-8.
    """
    execute_query(connection,"SET NAMES utf8;", commit=False)
    execute_query(connection,"SET character_set_client = utf8mb4;", commit=False)

def drop_tables(connection):
    """
    Drop all tables in the database.
    """
    drop_tables_query = '''
        DROP TABLE IF EXISTS seriespost, salaries, pitchingpost, pitching,
        managershalf, managers, homegames, parks, halloffame, fieldingpost,
        fieldingofsplit, fieldingof, fielding, collegeplaying, schools,
        battingpost, batting, awardsshareplayers, awardssharemanagers,
        awardsplayers, awardsmanagers, appearances, allstarfull, people,
        teamshalf, teams, teamsfranchises, divisions, leagues;
    '''
    execute_query(connection,drop_tables_query, commit=True)

def create_tables(connection):
    """
    Create all required tables. Load initial data into tables from CSV files or static queries.
    """
    create_leagues_table = '''
        CREATE TABLE leagues (
            lgID char(2) NOT NULL,
            league varchar(50) NOT NULL,
            active char NOT NULL,
            PRIMARY KEY (lgID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    execute_query(connection,create_leagues_table, commit=True)

    load_leagues_data = '''
        INSERT INTO leagues (lgID, league, active) VALUES
        ('ML', 'Major League', 'Y'), ('AL', 'American League', 'Y'),
        ('NL', 'National League', 'Y'), ('AA', 'American Association', 'N'),
        ('FL', 'Federal League', 'N'), ('NA', 'National Association', 'N'),
        ('PL', 'Players'' League', 'N'), ('UA', 'Union Association', 'N');
    '''
    execute_query(connection,load_leagues_data, commit=True)

    create_divisions_table = '''
        CREATE TABLE divisions (
            ID INT NOT NULL AUTO_INCREMENT,
            divID char(2) NOT NULL,
            lgID char(2) NOT NULL,
            division varchar(50) NOT NULL,
            active char NOT NULL,
            PRIMARY KEY (ID),
            UNIQUE KEY (divID, lgID),
            FOREIGN KEY (lgID) REFERENCES leagues(lgID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    execute_query(connection,create_divisions_table, commit=True)

    load_divisions_data = '''
        INSERT INTO divisions (divID, lgID, division, active) VALUES
        ('E', 'AL', 'AL East', 'Y'), ('W', 'AL', 'AL West', 'Y'),
        ('C', 'AL', 'AL Central', 'Y'), ('E', 'NL', 'NL East', 'Y'),
        ('W', 'NL', 'NL West', 'Y'), ('C', 'NL', 'NL Central', 'Y'),
        ('A', 'AA', 'Sole Division', 'N'), ('F', 'FL', 'Sole Division', 'N'),
        ('N', 'NA', 'Sole Division', 'N'), ('P', 'PL', 'Sole Division', 'N'),
        ('U', 'UA', 'Sole Division', 'N');
    '''
    execute_query(connection,load_divisions_data, commit=True)

    create_master_table = '''
        CREATE TABLE IF NOT EXISTS master (
            playerID VARCHAR(9) NOT NULL,
            birthYear SMALLINT(6) DEFAULT NULL,
            birthMonth TINYINT(4) DEFAULT NULL,
            birthDay TINYINT(4) DEFAULT NULL,
            birthCountry VARCHAR(50) DEFAULT NULL,
            birthState VARCHAR(50) DEFAULT NULL,
            birthCity VARCHAR(50) DEFAULT NULL,
            deathYear SMALLINT(6) DEFAULT NULL,
            deathMonth TINYINT(4) DEFAULT NULL,
            deathDay TINYINT(4) DEFAULT NULL,
            deathCountry VARCHAR(50) DEFAULT NULL,
            deathState VARCHAR(50) DEFAULT NULL,
            deathCity VARCHAR(50) DEFAULT NULL,
            nameFirst VARCHAR(50) DEFAULT NULL,
            nameLast VARCHAR(50) DEFAULT NULL,
            nameGiven VARCHAR(50) DEFAULT NULL,
            weight SMALLINT(6) DEFAULT NULL,
            height SMALLINT(6) DEFAULT NULL,
            bats CHAR(1) DEFAULT NULL,
            throws CHAR(1) DEFAULT NULL,
            debut DATE DEFAULT NULL,
            finalGame DATE DEFAULT NULL,
            retroID VARCHAR(9) DEFAULT NULL,
            bbrefID VARCHAR(9) DEFAULT NULL,
            PRIMARY KEY (playerID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    execute_query(connection,create_master_table, commit=True)

    load_master_data = f'''
        LOAD DATA LOCAL INFILE '{path}Master.csv'
        INTO TABLE master
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS;
    '''
    execute_query(connection,load_master_data, commit=True)

    create_teams_franchises_table = '''
        CREATE TABLE IF NOT EXISTS TeamsFranchises (
            franchID VARCHAR(3) NOT NULL,
            franchName VARCHAR(50) DEFAULT NULL,
            active CHAR DEFAULT NULL,
            NAassoc VARCHAR(3) DEFAULT NULL,
            PRIMARY KEY (franchID)
        );
    '''
    execute_query(connection,create_teams_franchises_table, commit=True)
    
    load_teams_franchises_data = f'''
        LOAD DATA LOCAL INFILE '{path}TeamsFranchises.csv'
        INTO TABLE TeamsFranchises
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS;
    '''
    execute_query(connection,load_teams_franchises_data, commit=True)

    create_teams_table = '''
        CREATE TABLE teams (
            ID INT NOT NULL AUTO_INCREMENT, /* ADDED BY WEBUCATOR */
            yearID smallint(6) NOT NULL,
            lgID char(2) DEFAULT NULL,
            teamID char(3) NOT NULL,
            franchID varchar(3) DEFAULT NULL,
            divID char(1) DEFAULT NULL,
            div_ID INT DEFAULT NULL, /* ADDED BY WEBUCATOR AS FK TO divisions TABLE*/
            teamRank smallint(6) DEFAULT NULL,
            G smallint(6) DEFAULT NULL,
            Ghome smallint(6) DEFAULT NULL,
            W smallint(6) DEFAULT NULL,
            L smallint(6) DEFAULT NULL,
            DivWin varchar(1) DEFAULT NULL,
            WCWin varchar(1) DEFAULT NULL,
            LgWin varchar(1) DEFAULT NULL,
            WSWin varchar(1) DEFAULT NULL,
            R smallint(6) DEFAULT NULL,
            AB smallint(6) DEFAULT NULL,
            H smallint(6) DEFAULT NULL,
            2B smallint(6) DEFAULT NULL,
            3B smallint(6) DEFAULT NULL,
            HR smallint(6) DEFAULT NULL,
            BB smallint(6) DEFAULT NULL,
            SO smallint(6) DEFAULT NULL,
            SB smallint(6) DEFAULT NULL,
            CS smallint(6) DEFAULT NULL,
            HBP smallint(6) DEFAULT NULL,
            SF smallint(6) DEFAULT NULL,
            RA smallint(6) DEFAULT NULL,
            ER smallint(6) DEFAULT NULL,
            ERA double DEFAULT NULL,
            CG smallint(6) DEFAULT NULL,
            SHO smallint(6) DEFAULT NULL,
            SV smallint(6) DEFAULT NULL,
            IPouts int(11) DEFAULT NULL,
            HA smallint(6) DEFAULT NULL,
            HRA smallint(6) DEFAULT NULL,
            BBA smallint(6) DEFAULT NULL,
            SOA smallint(6) DEFAULT NULL,
            E int(11) DEFAULT NULL,
            DP int(11) DEFAULT NULL,
            FP double DEFAULT NULL,
            name varchar(50) DEFAULT NULL,
            park varchar(255) DEFAULT NULL,
            attendance int(11) DEFAULT NULL,
            BPF int(11) DEFAULT NULL,
            PPF int(11) DEFAULT NULL,
            teamIDBR varchar(3) DEFAULT NULL,
            teamIDlahman45 varchar(3) DEFAULT NULL,
            teamIDretro varchar(3) DEFAULT NULL,
            PRIMARY KEY (ID),
            UNIQUE KEY (yearID,lgID,teamID),
            FOREIGN KEY (lgID) REFERENCES leagues(lgID), /* Not normalized, but keeping to maintain consistency with original */
            FOREIGN KEY (div_ID) REFERENCES divisions(ID),
            FOREIGN KEY (franchID) REFERENCES teamsfranchises(franchID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    execute_query(connection,create_teams_table, commit=True)

    load_teams_data = f'''
        LOAD DATA LOCAL INFILE '{path}Teams.csv'
        INTO TABLE teams
        FIELDS TERMINATED BY ',' 
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS
        (yearID, lgID, teamID, franchID, divID, teamRank, G, Ghome, W, L, DivWin, WCWin, LgWin, WSWin, R, AB, H, `2B`, `3B`, HR, BB, SO, SB, CS, HBP, SF, RA, ER, ERA, CG, SHO, SV, IPouts, HA, HRA, BBA, SOA, E, DP, FP, name, park, attendance, BPF, PPF, teamIDBR, teamIDlahman45, teamIDretro);
    '''
    execute_query(connection,load_teams_data, commit=True)

    create_teamshalf_table = '''
    CREATE TABLE teamshalf (
        ID INT NOT NULL AUTO_INCREMENT, /* ADDED BY WEBUCATOR */
        yearID smallint(6) NOT NULL,
        lgID char(2) NOT NULL,
        teamID char(3) NOT NULL,
        team_ID INT DEFAULT NULL, /* ADDED BY WEBUCATOR AS FK TO teams TABLE*/
        Half varchar(1) NOT NULL,
        divID char(1) DEFAULT NULL,
        div_ID INT DEFAULT NULL, /* ADDED BY WEBUCATOR AS FK TO divisions TABLE*/
        DivWin varchar(1) DEFAULT NULL,
        teamRank smallint(6) DEFAULT NULL,
        G smallint(6) DEFAULT NULL,
        W smallint(6) DEFAULT NULL,
        L smallint(6) DEFAULT NULL,
        PRIMARY KEY (ID),
        UNIQUE KEY (yearID,lgID,teamID,Half),
        FOREIGN KEY (lgID) REFERENCES leagues(lgID), /* Not normalized, but keeping to maintain consistency with original */
        FOREIGN KEY (div_ID) REFERENCES divisions(ID), /* Not normalized, but keeping to maintain consistency with original */
        FOREIGN KEY (team_ID) REFERENCES teams(ID)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    execute_query(connection,create_teamshalf_table, commit=True)

    load_teamshalf_data = f'''
        LOAD DATA LOCAL INFILE '{path}TeamsHalf.csv'
        INTO TABLE teamshalf
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS;
    '''
    execute_query(connection,load_teamshalf_data, commit=True)

    create_fielding_table = '''
        CREATE TABLE fielding (
            ID INT NOT NULL AUTO_INCREMENT,
            playerID VARCHAR(9) NOT NULL,
            yearID SMALLINT NOT NULL,
            stint SMALLINT NOT NULL,
            teamID CHAR(3),
            lgID CHAR(2),
            POS VARCHAR(2) NOT NULL,
            G SMALLINT,
            GS SMALLINT,
            InnOuts INT,
            PO SMALLINT,
            A SMALLINT,
            E SMALLINT,
            DP SMALLINT,
            PB SMALLINT,
            WP SMALLINT,
            SB SMALLINT,
            CS SMALLINT,
            ZR DOUBLE,
            PRIMARY KEY (ID),
            UNIQUE KEY (playerID, yearID, stint, POS)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


        '''
    execute_query(connection, create_fielding_table, commit=True)


    load_fielding_data = f'''
        LOAD DATA LOCAL INFILE '{path}Fielding.csv'
        INTO TABLE fielding
        FIELDS TERMINATED BY ',' ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS
        (playerID, yearID, stint, teamID, lgID, POS, G, GS, InnOuts, PO, A, E, DP, PB, WP, SB, CS, ZR);
    '''
    execute_query(connection, load_fielding_data, commit=True)

    create_batting_table = '''
        CREATE TABLE batting (
            ID INT NOT NULL AUTO_INCREMENT, /* ADDED BY WEBUCATOR */
            playerID varchar(9) NOT NULL,
            yearID smallint(6) NOT NULL,
            stint smallint(6) NOT NULL,
            teamID char(3) DEFAULT NULL,
            team_ID INT DEFAULT NULL, /* ADDED BY WEBUCATOR AS FK TO teams TABLE*/
            lgID char(2) DEFAULT NULL,
            G smallint(6) DEFAULT NULL,
            G_batting smallint(6) DEFAULT NULL,
            AB smallint(6) DEFAULT NULL,
            R smallint(6) DEFAULT NULL,
            H smallint(6) DEFAULT NULL,
            2B smallint(6) DEFAULT NULL,
            3B smallint(6) DEFAULT NULL,
            HR smallint(6) DEFAULT NULL,
            RBI smallint(6) DEFAULT NULL,
            SB smallint(6) DEFAULT NULL,
            CS smallint(6) DEFAULT NULL,
            BB smallint(6) DEFAULT NULL,
            SO smallint(6) DEFAULT NULL,
            IBB smallint(6) DEFAULT NULL,
            HBP smallint(6) DEFAULT NULL,
            SH smallint(6) DEFAULT NULL,
            SF smallint(6) DEFAULT NULL,
            GIDP smallint(6) DEFAULT NULL,
            PRIMARY KEY (ID),
            UNIQUE KEY (playerID,yearID,stint),
            FOREIGN KEY (lgID) REFERENCES leagues(lgID), /* Not normalized, but keeping to maintain consistency with original */
            FOREIGN KEY (team_ID) REFERENCES teams(ID),
            FOREIGN KEY (playerID) REFERENCES master(playerID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    execute_query(connection,create_batting_table, commit=True)

    load_batting_data = f'''
        LOAD DATA LOCAL INFILE '{path}Batting.csv'
        INTO TABLE Batting
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS;
    '''
    execute_query(connection,load_batting_data, commit=True)

    create_pitching_table = '''
        CREATE TABLE pitching (
            ID INT NOT NULL AUTO_INCREMENT,
            playerID VARCHAR(9) NOT NULL,
            yearID SMALLINT(6) NOT NULL,
            stint SMALLINT(6) NOT NULL,
            teamID INT(3) DEFAULT NULL,
            lgID CHAR(2) DEFAULT NULL,
            W SMALLINT(6) DEFAULT NULL,
            L SMALLINT(6) DEFAULT NULL,
            G SMALLINT(6) DEFAULT NULL,
            GS SMALLINT(6) DEFAULT NULL,
            CG SMALLINT(6) DEFAULT NULL,
            SHO SMALLINT(6) DEFAULT NULL,
            SV SMALLINT(6) DEFAULT NULL,
            IPOuts INT DEFAULT NULL,
            H SMALLINT(6) DEFAULT NULL,
            ER SMALLINT(6) DEFAULT NULL,
            HR SMALLINT(6) DEFAULT NULL,
            BB SMALLINT(6) DEFAULT NULL,
            SO SMALLINT(6) DEFAULT NULL,
            BAOpp FLOAT DEFAULT NULL,
            ERA FLOAT DEFAULT NULL,
            IBB SMALLINT(6) DEFAULT NULL,
            WP SMALLINT(6) DEFAULT NULL,
            HBP SMALLINT(6) DEFAULT NULL,
            BK SMALLINT(6) DEFAULT NULL,
            BFP SMALLINT(6) DEFAULT NULL,
            GF SMALLINT(6) DEFAULT NULL,
            R SMALLINT(6) DEFAULT NULL,
            SH SMALLINT(6) DEFAULT NULL,
            SF SMALLINT(6) DEFAULT NULL,
            GIDP SMALLINT(6) DEFAULT NULL,
            PRIMARY KEY (ID),
            UNIQUE KEY (playerID, yearID, stint),
            FOREIGN KEY (lgID) REFERENCES leagues(lgID),
            FOREIGN KEY (teamID) REFERENCES teams(ID),
            FOREIGN KEY (playerID) REFERENCES master(playerID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
    execute_query(connection,create_pitching_table, commit=True)

    load_pitching_data = f'''
        LOAD DATA LOCAL INFILE '{path}Pitching.csv'
        INTO TABLE Pitching
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS;
    '''
    execute_query(connection,load_pitching_data, commit=True)

@click.group()
def cli():
    """Database Management CLI"""
    pass

@cli.command("init-db")
def init_db():
    """
    Initialize the database: create schema, tables, and load data.
    """
    try:
        connection = get_db(use_database=False)
        create_database(connection)
        set_encoding(connection)
        create_tables(connection)
        connection.close()
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise RuntimeError("Failed to initialize the database.")

if __name__ == "__main__":
    cli()