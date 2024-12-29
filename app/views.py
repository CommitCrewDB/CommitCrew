from flask import render_template, request, redirect, url_for, flash, jsonify, app
from app.models.teams import Teams
from app.models.fielding import Fielding
from app.models.pitching import create_connection
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
    if request.method == 'POST':
        # Form verilerini al ve güncelle
        updated_data = {
            "Team": request.form.get("team_name", ""),
            "Rank": request.form.get("rank", 0),
            "Wins": request.form.get("wins", 0),
            "Losses": request.form.get("losses", 0),
            "TeamDivision": request.form.get("team_division", "N/A"),
            "GamesPlayed": request.form.get("games_played", 0),
        }


        Teams.update_team(team_id, updated_data)
        flash("Team updated successfully!", "success")
        return redirect(url_for('teams_page'))
    else:
        # Güncelleme formunu görüntülemek için takım verilerini al
        team = Teams.get_team_by_id(team_id)
        return render_template('updateteams.html', team=team)

def fielding_page():
    player_id = request.args.get("player_id", "")
    league = request.args.getlist("league")
    year = request.args.get("year", "")
    position = request.args.get("position", "")
    action = request.args.get("action")

    leagues = Teams.get_all_leagues()
    fielding_records = []

    if league or player_id or year or position:
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

    # Fetch existing record data
    record = Fielding.get_record_by_id(record_id)
    return render_template("updatefielding.html", record=record)

def delete_fielding_record(record_id):
    try:
        Fielding.delete_record(record_id)  # Implement this in your Fielding model
        flash("Fielding record deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while deleting the record: {e}", "danger")
    return redirect(url_for("fielding_page"))

def batting_page():
    year_query = request.args.get("year", "")
    team_query = request.args.get("team", "")
    league_query = request.args.getlist("league")
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
    elif year_query or team_query or league_query or sort_by:
        batting_records = Batting.search_batting(
            year=year_query,
            team=team_query,
            leagues=league_query,
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

def master_options():
    return render_template("master_options.html")

def master_table():
    action = request.args.get('action', 'view_all')
    search_query = request.args.get('search', '')

    if action == 'view_all':
        master_data = Master.load_master_data()
        return render_template("master.html", master_data=master_data)

    elif action == 'search' and search_query:
        # Search for specific data
        master_data = Master.search_and_sort(search_query=search_query)
        return render_template("master.html", master_data=master_data, search_query=search_query)

    # Default behavior: return to master options
    return redirect(url_for('master_options'))

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

def add_pitching_data():
    if request.method == 'POST':
        print("POST request received!")  # Debug
        print("Form Data:", request.form)  # Debug

        # Extract form data
        playerID = request.form.get('playerID')
        yearID = request.form.get('yearID')
        teamID = request.form.get('teamID')
        lgID = request.form.get('lgID')
        stint = request.form.get('stint')
        W = request.form.get('W')
        L = request.form.get('L')
        ERA = request.form.get('ERA')

        # Debug: Print field values
        print("Player ID:", playerID)
        print("Year ID:", yearID)
        print("Team ID:", teamID)
        print("League ID:", lgID)
        print("Stint:", stint)
        print("Wins:", W)
        print("Losses:", L)
        print("ERA:", ERA)

        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed!")  # Debug
                flash("Database connection failed.", "danger")
                return redirect(url_for('add_pitching_data'))

            with connection.cursor(dictionary=True) as cursor:
                # Check for duplicate data
                cursor.execute(
                    "SELECT * FROM pitching WHERE playerID = %s AND yearID = %s AND teamID = %s AND lgID = %s AND stint = %s",
                    (playerID, yearID, teamID, lgID, stint)
                )
                if cursor.fetchone():
                    print("Duplicate data found!")  # Debug
                    flash("Data already exists.", "danger")
                    return redirect(url_for('add_pitching_data'))

                # Insert new data
                query = """
                    INSERT INTO pitching (playerID, yearID, teamID, lgID, stint, W, L, ERA)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(query, (playerID, yearID, teamID, lgID, stint, W, L, ERA))
                connection.commit()

                print("Data successfully added!")  # Debug
                flash("Data has been successfully added.", "success")
                return redirect(url_for('pitching_page'))
        except Exception as e:
            print(f"Error occurred: {e}")  # Debug
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for('add_pitching_data'))

    return render_template('addpitching.html')

def update_pitching_data(id):
    if request.method == 'POST':
        print("POST request received for update!")  # Debug
        print("Form Data:", request.form)  # Debug

        # Extract form data
        playerName = request.form.get('playerName')
        yearID = request.form.get('yearID')
        teamID = request.form.get('teamID')
        lgID = request.form.get('lgID')
        stint = request.form.get('stint')
        W = request.form.get('W')
        L = request.form.get('L')
        ERA = request.form.get('ERA')

        # Debug: Print field values
        print("Player Name:", playerName)
        print("Year ID:", yearID)
        print("Team ID:", teamID)
        print("League ID:", lgID)
        print("Stint:", stint)
        print("Wins:", W)
        print("Losses:", L)
        print("ERA:", ERA)

        try:
            connection = create_connection()
            if connection is None:
                print("Database connection failed!")  # Debug
                flash("Database connection failed.", "danger")
                return redirect(url_for('update_pitching_data', id=id))

            with connection.cursor(dictionary=True) as cursor:
                # Debug: Validate player name lookup
                print(f"Looking for player: {playerName}")
                cursor.execute("SELECT playerID FROM master WHERE CONCAT(nameFirst, ' ', nameLast) = %s", (playerName,))
                player = cursor.fetchone()

                if not player:
                    print("Player not found!")  # Debug
                    flash("Player name not found in the master table.", "danger")
                    return redirect(url_for('update_pitching_data', id=id))

                playerID = player['playerID']
                print(f"Found playerID: {playerID}")

                # Update data
                query = """
                    UPDATE pitching
                    SET yearID = %s, teamID = %s, lgID = %s, stint = %s, W = %s, L = %s, ERA = %s
                    WHERE playerID = %s AND id = %s
                """
                print("Executing query:", query)  # Debug
                print("With values:", (yearID, teamID, lgID, stint, W, L, ERA, playerID, id))  # Debug
                cursor.execute(query, (yearID, teamID, lgID, stint, W, L, ERA, playerID, id))
                connection.commit()

                print("Data successfully updated!")  # Debug
                flash("Data has been successfully updated.", "success")
                return redirect(url_for('pitching_page'))
        except Exception as e:
            print(f"Error occurred: {e}")  # Debug
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for('update_pitching_data', id=id))

    # Fetch existing data to pre-fill the form
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
    except Exception as e:
        print(f"Error occurred: {e}")  # Debug
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('pitching_page'))

    return render_template('updatepitching.html', data=data)

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