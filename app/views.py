from flask import render_template, request, redirect, url_for, flash, jsonify, app
from app.models.teams import Teams
from app.models.fielding import Fielding
from app.models.pitching import create_connection, Pitching
from app.models.batting import Batting
from app.models.master import Master
import logging

def home_page():
    return render_template("home.html")

def teams_page():
    search_query = request.args.get("search", "")
    league_filters = request.args.getlist("league")
    year_filter = request.args.get("year", "")
    team_name_filter = request.args.get("team_name", "")
    action = request.args.get('action')
    sort_by = request.args.get("sort_by", "")

    leagues = Teams.get_all_leagues()

    teams = []
    if action == 'view_all':
        teams = Teams.get_all_teams()
        return render_template("teams.html", teams=teams, leagues=leagues)
    if league_filters or year_filter or team_name_filter or sort_by:
        teams = Teams.filter_teams(
            leagues=league_filters,
            year=year_filter,
            team_name=team_name_filter,
            sort_by=sort_by
        )
    if search_query:
        teams = Teams.search_by_name(search_query)

    if action == 'view_top_teams_byLeague':
        top_teams_league = Teams.get_top_teams_by_league()
        return render_template("teams.html", top_teams_league=top_teams_league)

    if action == 'view_top_teams_byYear':
        top_teams_year = Teams.get_top_teams_by_year()
        return render_template("teams.html", top_teams_year=top_teams_year)
    
    if request.method == "POST":
        action = request.form.get("action")
        team_id = request.form.get("team_id")

        if action == "delete":
            if not team_id:
                flash("Team ID is required to delete a team.", "danger")
            else:
                try:
                    Teams.delete_team(team_id)
                    flash(f"Team with ID {team_id} deleted successfully!", "success")
                except Exception as e:
                    print(f"Error while deleting team: {e}")
                    flash(f"An error occurred while deleting team: {e}", "danger")
            return redirect(url_for("teams_page"))

    return render_template("teams.html", teams=teams, leagues=leagues)

def add_team_page():
    if request.method == "POST":
        year = request.form.get("year")
        league = request.form.get("league")
        team_name = request.form.get("team_name")
        team_id = request.form.get("team_id")
        franchise = request.form.get("franchise")
        wins = request.form.get("wins")
        losses = request.form.get("losses")


        try:
            team_data = {
                "yearID": year,
                "League": league,
                "Team": team_name,
                "TeamID": team_id,
                "Franchise": franchise,
                "Wins": wins,
                "Losses": losses,
            }
            Teams.add_team(team_data)
            flash("New team added successfully!", "success")
            return redirect(url_for("teams_page"))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    return render_template("addteams.html")

def update_team_page(team_id):
    if request.method == "POST":
        updated_data = {
            "Year": request.form.get("year"),
            "League": request.form.get("league"),
            "TeamID": request.form.get("team_id"),
            "Team": request.form.get("team_name"),
            "Franchise": request.form.get("franchise"),
            "Wins": request.form.get("wins"),
            "Losses": request.form.get("losses"),
        }
        try:
            Teams.update_team(team_id, updated_data)
            flash("Team updated successfully!", "success")
            return redirect(url_for("teams_page"))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    team = Teams.get_team_by_id(team_id)
    return render_template("updateteams.html", team=team)

def delete_team(team_id):
    try:
        Teams.delete_team(team_id)
        flash("Team deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while deleting the team: {e}", "danger")
    return redirect(url_for("teams_page"))


def fielding_page():
    player_id = request.args.get("player_id", "")
    league = request.args.getlist("league")
    year = request.args.get("year", "")
    position = request.args.get("position", "")
    action = request.args.get("action", "")

    leagues = Teams.get_all_leagues()
    fielding_records = []
    top_fielding_players = []

    if action == "view_all_data":
        fielding_records = Fielding.get_all_fielding()
    elif action == "view_top_players":
        top_fielding_players = Fielding.get_top_fielding_players(year)
    elif player_id or league or year or position:
        fielding_records = Fielding.filter_fielding(
            leagues=league,
            player_id=player_id,
            year=year,
            position=position
        )

    return render_template(
        "fielding.html",
        fielding_records=fielding_records,
        leagues=leagues,
        player_id=player_id,
        year=year,
        position=position,
        top_fielding_players=top_fielding_players
    )

def add_fielding_page():
    if request.method == "POST":
        player_id = request.form.get("player_id")
        year = request.form.get("year")
        stint = request.form.get("stint")
        team_id = request.form.get("team_id")
        league = request.form.get("league")
        position = request.form.get("position")
        games = request.form.get("games")
        po = request.form.get("po")

        try:
            fielding_data = {
                "player_id": player_id,
                "year": year,
                "stint": stint,
                "team_id": team_id,
                "league": league,
                "position": position,
                "games": games,
                "po": po,
            }
            Fielding.add_fielding_record(fielding_data)
            flash("Fielding record added successfully!", "success")
            return redirect(url_for("fielding_page"))
        except ValueError as ve:
            flash(str(ve), "warning")  # Flash specific validation error
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
    return render_template("addfielding.html")

def update_fielding_page(record_id):
    if request.method == "POST":
        updated_data = {
            "playerID": request.form.get("player_id"),
            "yearID": request.form.get("year"),
            "stint": request.form.get("stint"),
            "teamID": request.form.get("team_id"),
            "lgID": request.form.get("league"),
            "POS": request.form.get("position"),
            "G": request.form.get("games"),
            "PO": request.form.get("po"),
        }
        try:
            Fielding.update_record(record_id, updated_data)
            flash("Fielding record updated successfully!", "success")
            return redirect(url_for("fielding_page"))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    record = Fielding.get_record_by_id(record_id)
    return render_template("updatefielding.html", record=record)

def delete_fielding_record(record_id):
    try:
        Fielding.delete_record(record_id) 
        flash("Fielding record deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while deleting the record: {e}", "danger")
    return redirect(url_for("fielding_page"))




def batting_page():
    year_query = request.args.get("year", "")
    team_query = request.args.get("team", "")
    league_query = request.args.getlist("league")
    player_query = request.args.get("player", "")
    sort_by = request.args.get("sort_by", "")
    sort_order = request.args.get("sort_order", "asc")
    action = request.args.get("action", "")

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    offset = (page - 1) * per_page

    leagues = Batting.get_leagues()
    active_leagues = [league for league in leagues if league["active"] == "Y"]
    inactive_leagues = [league for league in leagues if league["active"] != "Y"]

    if action == "view_all_data":
        total_records = Batting.get_total_batting_records()
        batting_records = Batting.get_paginated_batting(offset, per_page)
    elif year_query or team_query or league_query or player_query or sort_by:
        batting_records = Batting.search_batting(
            year=year_query,
            team=team_query,
            leagues=league_query,
            player=player_query,
            sort_by=sort_by,
            sort_order=sort_order
        )
        total_records = len(batting_records)
        batting_records = batting_records[offset:offset + per_page]
    else:
        batting_records = []
        total_records = 0

    total_pages = (total_records + per_page - 1) // per_page
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    return render_template(
        "batting.html",
        batting_records=batting_records,
        year_query=year_query,
        team_query=team_query,
        league_query=league_query,
        player_query=player_query,
        sort_by=sort_by,
        sort_order=sort_order,
        active_leagues=active_leagues,
        inactive_leagues=inactive_leagues,
        current_page=page,
        per_page=per_page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        action=action,
    )

def add_batting_record():
    if request.method == "POST":
        try:
            player_id = request.form.get("playerID")
            year_id = request.form.get("yearID")
            stint = request.form.get("stint")
            team_id = request.form.get("teamID") or None
            lg_id = request.form.get("lgID") or None
            stat_fields = [
                "G", "AB", "R", "H", "2B", "3B", "HR", "RBI", 
                "SB", "CS", "BB", "SO", "IBB", "HBP", "SH", "SF", "GIDP"
            ]
            stats = {field: request.form.get(field) or 0 for field in stat_fields if field in request.form}

            Batting.insert(player_id, year_id, stint, team_id, lg_id, **stats)
            flash("Batting record added successfully!", "success")
            return redirect(url_for("batting_page"))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    return render_template("batting-add.html")

def update_batting_record(record_id):
    if request.method == "POST":
        try:
            allowed_fields = [
                "G", "AB", "R", "H", "2B", "3B", "HR", "RBI", 
                "SB", "CS", "BB", "SO", "IBB", "HBP", "SH", "SF", "GIDP"
            ]
            record = Batting.get_by_id(record_id)

            if not record:
                flash("Record not found!", "danger")
                return redirect(url_for("batting_page"))

            stats = {}
            for field in allowed_fields:
                new_value = request.form.get(field) or 0
                existing_value = record.get(field) or 0

                if str(new_value) != str(existing_value):
                    stats[field] = new_value

            if not stats:
                flash("No changes detected. Record not updated.", "info")
                return redirect(url_for("update_batting_record", record_id=record_id))

            Batting.update(record_id, **stats)
            flash("Batting record updated successfully!", "success")
            return redirect(url_for("batting_page"))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    record = Batting.get_by_id(record_id)

    if not record:
        flash("Record not found!", "danger")
        return redirect(url_for("batting_page"))

    return render_template("batting-update.html", record=record)

def delete_batting_record(record_id):
    if request.method == "POST":
        try:
            Batting.delete(record_id)
            flash("Batting record deleted successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
    else:
        flash("Invalid request method for deletion.", "danger")
    return redirect(url_for("batting_page"))
from flask import request, render_template, flash, redirect, url_for

def master_page():
    search_query = request.args.get("search", "")
    action = request.args.get('action')
    sort_by = request.args.get("sort_by", "")

    players = []
    if action == 'view_all':
        players = Master.get_all_players()
        return render_template("master.html", players=players)

    if search_query:
        players = Master.search_by_name(search_query)

    if action == 'view_top_players':
        top_players = Master.get_top_players()
        return render_template("master.html", top_players=top_players)
    
    if request.method == "POST":
        action = request.form.get("action")
        player_id = request.form.get("player_id")

        if action == "delete":
            if not player_id:
                flash("Player ID is required to delete a player.", "danger")
            else:
                try:
                    Master.delete_player(player_id)
                    flash(f"Player with ID {player_id} deleted successfully!", "success")
                except Exception as e:
                    print(f"Error while deleting player: {e}")
                    flash(f"An error occurred while deleting player: {e}", "danger")
            return redirect(url_for("master_page"))

    return render_template("master.html", players=players)

def add_player_page():
    if request.method == "POST":
        name_first = request.form.get("nameFirst")
        name_last = request.form.get("nameLast")
        birth_year = request.form.get("birthYear")
        birth_month = request.form.get("birthMonth")
        birth_day = request.form.get("birthDay")
        weight = request.form.get("weight")
        height = request.form.get("height")
        bats = request.form.get("bats")
        throws = request.form.get("throws")
        debut = request.form.get("debut")
        final_game = request.form.get("finalGame")
        bbref_id = request.form.get("bbrefID")
        retro_id = request.form.get("retroID")

        try:
            player_data = {
                "nameFirst": name_first,
                "nameLast": name_last,
                "birthYear": birth_year,
                "birthMonth": birth_month,
                "birthDay": birth_day,
                "weight": weight,
                "height": height,
                "bats": bats,
                "throws": throws,
                "debut": debut,
                "finalGame": final_game,
                "bbrefID": bbref_id,
                "retroID": retro_id,
            }
            Master.add_player(player_data)
            flash("New player added successfully!", "success")
            return redirect(url_for("master_page"))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    return render_template("addmaster.html")

def update_player_page(player_id):
    if request.method == 'POST':
        # Form verilerini al ve güncelle
        updated_data = {
            "nameFirst": request.form.get("nameFirst", ""),
            "nameLast": request.form.get("nameLast", ""),
            "birthYear": request.form.get("birthYear", 0),
            "birthMonth": request.form.get("birthMonth", 0),
            "birthDay": request.form.get("birthDay", 0),
            "weight": request.form.get("weight", 0),
            "height": request.form.get("height", 0),
            "bats": request.form.get("bats", ""),
            "throws": request.form.get("throws", ""),
            "debut": request.form.get("debut", ""),
            "finalGame": request.form.get("finalGame", ""),
            "bbrefID": request.form.get("bbrefID", ""),
            "retroID": request.form.get("retroID", ""),
        }

        Master.update_player(player_id, updated_data)
        flash("Player updated successfully!", "success")
        return redirect(url_for('master_page'))
    else:
        # Güncelleme formunu görüntülemek için oyuncu verilerini al
        player = Master.get_player_by_id(player_id)
        return render_template('update_master.html', player=player)


def about_page():
    return render_template("about.html")

def pitching_page():
    sort_by = request.args.get('sort_by', '')  # Default to no sorting
    order = request.args.get('order', '')  # Default to no specific order

    # Filtering parameters
    search_name = request.args.get('search_name', '')
    search_year = request.args.get('search_year', '')
    search_league = request.args.get('search_league', '')
    action = request.args.get('action', '')

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 30

    connection = create_connection()
    if connection is None:
        print("Database connection failed.")
        return []

    cursor = connection.cursor(dictionary=True)

    # Get column names
    cursor.execute("SHOW COLUMNS FROM pitching")
    columns = [col['Field'] for col in cursor.fetchall() if col['Field'] != 'playerID']

    data = []
    total_records = 0
    if action == 'get_data':
        # Build the query with a join to get player names and league names
        query = """
            SELECT p.ID, pl.nameFirst, pl.nameLast, p.yearID, t.name AS teamName, l.league AS leagueName, p.W, p.L, p.ERA, p.SO AS strikeouts, p.BB AS walks, p.IPouts AS inningsPitched
            FROM pitching p
            INNER JOIN master pl ON p.playerID = pl.playerID
            INNER JOIN teams t ON p.teamID = t.teamID
            INNER JOIN leagues l ON p.lgID = l.lgID
        """
        conditions = []
        if search_name:
            conditions.append(f"(pl.nameFirst LIKE '%{search_name}%' OR pl.nameLast LIKE '%{search_name}%')")
        if search_year:
            conditions.append(f"p.yearID = '{search_year}'")
        if search_league:
            conditions.append(f"l.league LIKE '%{search_league}%'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        if sort_by and order:
            query += f" ORDER BY {sort_by} {order.upper()}"
        
        query += f" LIMIT %s OFFSET %s"

        print("Executing query:", query)
        print("With parameters:", (per_page, (page - 1) * per_page))

        cursor.execute(query, (per_page, (page - 1) * per_page))
        data = cursor.fetchall()

        # Get total number of records for pagination
        cursor.execute("SELECT COUNT(*) FROM pitching")
        total_records = cursor.fetchone()['COUNT(*)']

    connection.close()

    total_pages = (total_records + per_page - 1) // per_page

    return render_template('pitching.html', data=data, columns=columns, page=page, total_pages=total_pages, search_name=search_name, search_year=search_year, search_league=search_league, sort_by=sort_by, order=order, action=action)

def pitching_page():
    # Fetch query parameters
    year = request.args.get("year", "").strip()
    player_name = request.args.get("playerName", "").strip()
    league = request.args.get("league", "").strip()
    sort_by = request.args.get("sort_by", "yearID")  # Default sort column
    order = request.args.get("order", "asc")  # Default sort order
    page = request.args.get("page", 1, type=int)  # Current page number
    per_page = 10  # Number of rows per page
    show_data = request.args.get("show_data", None)

    results = []
    total_records = 0
    leaderboard_data = []
    leagues = []

    try:
        # Establish database connection
        connection = create_connection()
        if connection is None:
            flash("Database connection failed.", "danger")
            return redirect(url_for("pitching_page"))

        cursor = connection.cursor(dictionary=True)

        # Fetch league names
        league_query = """
            SELECT DISTINCT lgID, league
            FROM leagues
        """
        cursor.execute(league_query)
        leagues = cursor.fetchall()

        # Validate sort_by and order inputs
        valid_sort_columns = [
            "yearID", "playerID", "W", "L", "ERA", "G", "GS", "CG", "SHO", "SV",
            "IPouts", "H", "ER", "HR", "BB", "SO", "BAOpp"
        ]
        if sort_by not in valid_sort_columns:
            sort_by = "yearID"
        if order.lower() not in ["asc", "desc"]:
            order = "asc"

        # Fetch leaderboard data: Top 10 ERA
        leaderboard_query = """
            SELECT pl.nameFirst, pl.nameLast, t.name AS teamName, p.ERA
            FROM pitching p
            INNER JOIN master pl ON p.playerID = pl.playerID
            INNER JOIN teams t ON p.teamID = t.teamID
            WHERE p.ERA IS NOT NULL
            ORDER BY p.ERA ASC
            LIMIT 10
        """
        cursor.execute(leaderboard_query)
        leaderboard_data = cursor.fetchall()

        if show_data:  # Fetch data only when "Show Data" is clicked
            # Base query for fetching results
            query = """
                SELECT 
                    p.id, pl.nameFirst, pl.nameLast, p.yearID, p.stint, t.name AS teamName, l.league AS leagueName, 
                    p.W, p.L, p.ERA, p.G, p.GS, p.CG, p.SHO, p.SV, 
                    p.IPouts, p.H, p.ER, p.HR, p.BB, p.SO, p.BAOpp
                FROM pitching p
                INNER JOIN master pl ON p.playerID = pl.playerID
                INNER JOIN teams t ON p.teamID = t.teamID
                INNER JOIN leagues l ON p.lgID = l.lgID
                WHERE 1=1
            """
            count_query = """
                SELECT COUNT(*) AS total
                FROM pitching p
                INNER JOIN master pl ON p.playerID = pl.playerID
                INNER JOIN teams t ON p.teamID = t.teamID
                INNER JOIN leagues l ON p.lgID = l.lgID
                WHERE 1=1
            """
            params = []
            count_params = []

            # Add filter for year if provided
            if year:
                query += " AND p.yearID = %s"
                count_query += " AND p.yearID = %s"
                params.append(year)
                count_params.append(year)

            # Add filter for playerName if provided
            if player_name:
                query += " AND (pl.nameFirst LIKE %s OR pl.nameLast LIKE %s)"
                count_query += " AND (pl.nameFirst LIKE %s OR pl.nameLast LIKE %s)"
                params.extend([f"%{player_name}%", f"%{player_name}%"])
                count_params.extend([f"%{player_name}%", f"%{player_name}%"])

            # Add filter for league if provided
            if league:
                query += " AND l.lgID = %s"
                count_query += " AND l.lgID = %s"
                params.append(league)
                count_params.append(league)

            # Sorting and Pagination
            query += f" ORDER BY {sort_by} {order.upper()} LIMIT %s OFFSET %s"
            offset = (page - 1) * per_page
            params.extend([per_page, offset])

            # Execute main query
            cursor.execute(query, params)
            results = cursor.fetchall()

            # Execute count query
            cursor.execute(count_query, count_params)
            total_records = cursor.fetchone()["total"]

        # Calculate total pages
        total_pages = (total_records + per_page - 1) // per_page

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

    # Render template
    return render_template(
        "pitching.html",
        data=results,
        year=year,
        player_name=player_name,
        sort_by=sort_by,
        order=order,
        page=page,
        total_pages=total_pages,
        leaderboard=leaderboard_data,
        leagues=leagues,
    )


def add_pitching_page():
    if request.method == 'POST':
        try:
            data = {
                'playerID': request.form.get('playerID'),
                'yearID': request.form.get('yearID'),
                'stint': request.form.get('stint'),
                'teamID': request.form.get('teamID'),
                'lgID': request.form.get('lgID'),
                'W': request.form.get('W') or 0,
                'L': request.form.get('L') or 0,
                'ERA': request.form.get('ERA') or 0.0,
                'G': request.form.get('G') or 0,
                'GS': request.form.get('GS') or 0,
                'CG': request.form.get('CG') or 0,
                'SHO': request.form.get('SHO') or 0,
                'SV': request.form.get('SV') or 0,
                'IPouts': request.form.get('IPouts') or 0,
                'H': request.form.get('H') or 0,
                'ER': request.form.get('ER') or 0,
                'HR': request.form.get('HR') or 0,
                'BB': request.form.get('BB') or 0,
                'SO': request.form.get('SO') or 0,
                'BAOpp': request.form.get('BAOpp') or 0.0,
            }

            print(f"Form data received: {data}")  # Debug message
            
            success = Pitching.add_pitching(data)
            if success:
                flash("Successfully added a new record!", "success")
            else:
                flash("Failed to add pitching data.", "danger")
        except Exception as e:
            flash(f"An error occurred while adding the record: {e}", "danger")
            print(f"Error: {e}")  # Debug message

        return redirect(url_for('pitching_page'))

    return render_template('add_pitching.html')

def delete_pitching_data(id):
    try:
        connection = create_connection()
        if connection is None:
            print("Database connection failed!")  # Debug
            flash("Database connection failed.", "danger")
            return redirect(url_for('pitching_page'))

        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM pitching WHERE id = %s", (id,))
            data = cursor.fetchone()
            if not data:
                flash("Data not found.", "danger")
                return redirect(url_for('pitching_page'))

            cursor.execute("DELETE FROM pitching WHERE id = %s", (id,))
            connection.commit()

            print("Data successfully deleted!")  # Debug
            flash("Data has been successfully deleted.", "success")
    except Exception as e:
        print(f"Error occurred: {e}")  # Debug
        flash(f"An error occurred: {e}", "danger")

    return redirect(url_for('pitching_page'))

def update_pitching_data(id):
    if request.method == 'GET':
        try:
            connection = create_connection()
            if not connection:
                flash("Database connection failed.", "danger")
                return redirect(url_for('pitching_page'))

            # Fetch the existing data for the given ID
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT DISTINCT id, playerID, yearID, teamID, lgID, stint, W, L, ERA, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, SO, BAOpp  FROM pitching WHERE id = %s", (id,))
                data = cursor.fetchone()

            if not data:
                flash("No data found for the given ID.", "danger")
                return redirect(url_for('pitching_page'))

            # Debugging: Ensure fetched data includes 'id'
            print(f"Fetched data for ID {id}: {data}")

            return render_template('update_pitching.html', data=data)

        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            print(f"Error: {e}")
            return redirect(url_for('pitching_page'))

    elif request.method == 'POST':
        updated_data = {
            "playerID": request.form.get("playerID"),
            "yearID": request.form.get("yearID"),
            "teamID": request.form.get("teamID"),
            "lgID": request.form.get("lgID"),
            "stint": request.form.get("stint"),
            "W": request.form.get("W"),
            "L": request.form.get("L"),
            "ERA": request.form.get("ERA"),
            "G": request.form.get("G"),
            "GS": request.form.get("GS"),
            "CG": request.form.get("CG"),
            "SHO": request.form.get("SHO"),
            "SV": request.form.get("SV"),
            "IPouts": request.form.get("IPouts"),
            "H": request.form.get("H"),
            "ER": request.form.get("ER"),
            "HR": request.form.get("HR"),
            "BB": request.form.get("BB"),
            "SO": request.form.get("SO"),
            "BAOpp": request.form.get("BAOpp"),
        }
        # Call the Pitching update function
        success = Pitching.update_pitching(record_id=id, updated_data=updated_data)
        if success:
            flash("Data updated successfully!", "success")
        else:
            flash("Failed to update data.", "danger")

    return redirect(url_for('pitching_page'))