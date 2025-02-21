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
    if league_filters or year_filter or team_name_filter or sort_by:
        teams = Teams.filter_teams(
            leagues=league_filters,
            year=year_filter,
            team_name=team_name_filter,
            sort_by=sort_by
        )
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
    sort_by = request.args.get("sort_by", "")
    sort_order = request.args.get("sort_order", "asc")
    action = request.args.get("action", "")

    leagues = Teams.get_all_leagues()
    fielding_records = []
    top_fielding_players = []

    if action == "view_top_players":
        top_fielding_players = Fielding.get_top_fielding_players(year)
    elif player_id or league or year or position or sort_by:
        fielding_records = Fielding.filter_fielding(
            leagues=league,
            player_id=player_id,
            year=year,
            position=position,
            sort_by=sort_by,
            sort_order=sort_order
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

    batting_records = []
    total_records = 0
    batting_avg_by_year = []
    batting_avg_by_team = []
    batting_avg_by_league = []

    if action == "view_all_data":
        total_records = Batting.get_total_batting_records()
        batting_records = Batting.get_paginated_batting(offset, per_page)
    elif action == "search":
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
    elif action == "view_batting_average_by_year":
        batting_avg_by_year = Batting.get_batting_average_by_year()
        total_records = len(batting_avg_by_year)
        batting_avg_by_year = batting_avg_by_year[offset:offset + per_page]
    elif action == "view_batting_average_by_team":
        batting_avg_by_team = Batting.get_batting_average_by_team()
        total_records = len(batting_avg_by_team)
        batting_avg_by_team = batting_avg_by_team[offset:offset + per_page]
    elif action == "view_batting_average_by_league":
        batting_avg_by_league = Batting.get_batting_average_by_league()
        total_records = len(batting_avg_by_league)
        batting_avg_by_league = batting_avg_by_league[offset:offset + per_page]

    total_pages = (total_records + per_page - 1) // per_page
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    return render_template(
        "batting.html",
        batting_records=batting_records,
        batting_avg_by_year=batting_avg_by_year,
        batting_avg_by_team=batting_avg_by_team,
        batting_avg_by_league=batting_avg_by_league,
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

def master_page():
    search_query = request.args.get("search", "")
    birth_country_filter = request.args.get("birth_country", "")
    birth_year_filter = request.args.get("birth_year", "")
    death_year_filter = request.args.get("death_year", "")
    player_name_filter = request.args.get("player_name", "")
    sort_by = request.args.get("sort_by", "")
    action = request.args.get("action", "")

    players = []

    if birth_country_filter or birth_year_filter or death_year_filter or player_name_filter or sort_by:
        players = Master.filter_master(
            birth_country=birth_country_filter,
            birth_year=birth_year_filter,
            death_year=death_year_filter,
            player_name=player_name_filter,
            sort_by=sort_by
        )
    if search_query:
        players = Master.search_by_name(search_query)

    if action == 'view_top_players_byLeague':
        top_players_league = Master.get_top_players_by_league("stat", top_n=10)
        return render_template("master.html", top_players_league=top_players_league)

    if action == 'view_top_players_byYear':
        year = request.args.get("year", 1900)  # Örnek varsayılan yıl
        top_players_year = Master.get_top_players_by_year("stat", year, top_n=10)
        return render_template("master.html", top_players_year=top_players_year)

    return render_template("master.html", players=players)


def add_master_page():
    if request.method == "POST":
        try:
            player_data = {
                "playerID": request.form.get("player_id"),
                "birthYear": request.form.get("birth_year"),
                "birthMonth": request.form.get("birth_month"),
                "birthDay": request.form.get("birth_day"),
                "birthCity": request.form.get("birth_city"),
                "birthCountry": request.form.get("birth_country"),
                "birthState": request.form.get("birth_state"),
                "deathYear": request.form.get("death_year"),
                "deathMonth": request.form.get("death_month"),
                "deathDay": request.form.get("death_day"),
                "deathCountry": request.form.get("death_country"),
                "deathState": request.form.get("death_state"),
                "deathCity": request.form.get("death_city"),
                "nameFirst": request.form.get("first_name"),
                "nameLast": request.form.get("last_name"),
                "nameGiven": request.form.get("given_name"),
                "weight": request.form.get("weight"),
                "height": request.form.get("height"),
                "bats": request.form.get("bats"),
                "throws": request.form.get("throws"),
                "debut": request.form.get("debut"),
                "bbrefID": request.form.get("bbref_id"),
                "finalGame": request.form.get("final_game"),
                "retroID": request.form.get("retro_id"),
            }
            Master.add_player(player_data)
            flash("New player added successfully!", "success")
            return redirect(url_for("master_page"))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    return render_template("addmaster.html")


def update_master_page(player_id):
    if request.method == "POST":
        try:
            updated_data = {
                "nameFirst": request.form.get("first_name"),
                "nameLast": request.form.get("last_name"),
                "birthYear": request.form.get("birth_year"),
                "birthMonth": request.form.get("birth_month"),
                "birthDay": request.form.get("birth_day"),
                "weight": request.form.get("weight"),
                "height": request.form.get("height"),
            }
            Master.update_player(player_id, updated_data)
            flash("Player updated successfully!", "success")
            return redirect(url_for("master_page"))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    player = Master.get_player_by_id(player_id)
    return render_template("update_master.html", player=player)


def delete_master(player_id):
    try:
        Master.delete_player(player_id)
        flash("Player deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while deleting the player: {e}", "danger")

    return redirect(url_for("master_page"))


def about_page():
    return render_template("about.html")


def pitching_page():
    year = request.args.get("year", "").strip()
    player_name = request.args.get("playerName", "").strip()
    league = request.args.get("league", "").strip()
    sort_by = request.args.get("sort_by", "yearID")
    order = request.args.get("order", "asc")
    page = request.args.get("page", 1, type=int)
    per_page = 10
    show_data = request.args.get("show_data", None)

    results = []
    total_records = 0
    total_pages = 0
    leagues = []

    try:
        connection = create_connection()
        if connection is None:
            flash("Database connection failed.", "danger")
            return redirect(url_for("pitching_page"))

        cursor = connection.cursor(dictionary=True)

        # Fetch leagues once
        cursor.execute("SELECT DISTINCT league FROM leagues")
        leagues = [row["league"] for row in cursor.fetchall()]

        valid_sort_columns = [
            "yearID", "playerID", "W", "L", "ERA", "G", "GS", "CG", "SHO", "SV",
            "IPouts", "H", "ER", "HR", "BB", "SO", "BAOpp"
        ]
        if sort_by not in valid_sort_columns:
            sort_by = "yearID"
        if order.lower() not in ["asc", "desc"]:
            order = "asc"

        if show_data:
            query = """
                SELECT 
                    p.id, pl.nameFirst, pl.nameLast, p.yearID, p.stint, 
                    t.name AS teamName, l.league AS leagueName, 
                    p.W, p.L, p.ERA, p.G, p.GS, p.CG, p.SHO, p.SV, 
                    p.IPouts, p.H, p.ER, p.HR, p.BB, p.SO, p.BAOpp
                FROM pitching p
                LEFT JOIN master pl ON p.playerID = pl.playerID
                LEFT JOIN teams t ON p.teamID = t.teamID
                    AND p.yearID = t.yearID
                    AND p.lgID = t.lgID
                LEFT JOIN leagues l ON p.lgID = l.lgID
                WHERE 1=1
            """
            count_query = """
                SELECT COUNT(*) AS total
                FROM pitching p
                LEFT JOIN leagues l ON p.lgID = l.lgID
                WHERE 1=1
            """
            params = []
            count_params = []

            # Add year filter
            if year.isdigit():
                year = int(year)
                query += " AND p.yearID = %s"
                count_query += " AND p.yearID = %s"
                params.append(year)
                count_params.append(year)

            # Add player name filter
            if player_name:
                query += " AND (pl.nameFirst LIKE %s OR pl.nameLast LIKE %s)"
                count_query += " AND (pl.nameFirst LIKE %s OR pl.nameLast LIKE %s)"
                params.extend([f"%{player_name}%", f"%{player_name}%"])
                count_params.extend([f"%{player_name}%", f"%{player_name}%"])

            # Add league filter
            if league:
                query += " AND l.league = %s"
                count_query += " AND l.league = %s"
                params.append(league)
                count_params.append(league)

            # Sorting and Pagination
            offset = (page - 1) * per_page
            query += f" ORDER BY {sort_by} {order.upper()} LIMIT %s OFFSET %s"
            params.extend([per_page, offset])

            cursor.execute(query, params)
            results = cursor.fetchall()

            cursor.execute(count_query, count_params)
            total_records = cursor.fetchone()["total"]

        total_pages = (total_records + per_page - 1) // per_page

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

    return render_template(
        "pitching.html",
        data=results,
        year=year,
        player_name=player_name,
        league=league,
        sort_by=sort_by,
        order=order,
        page=page,
        total_pages=total_pages,
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

            # Establish database connection
            connection = create_connection()
            if not connection:
                flash("Database connection failed.", "danger")
                return redirect(url_for('pitching_page'))

            with connection.cursor(dictionary=True) as cursor:
                # Check for duplicate entry
                check_query = """
                    SELECT COUNT(*) AS count FROM pitching 
                    WHERE playerID = %s AND yearID = %s AND stint = %s
                """
                cursor.execute(check_query, (data["playerID"], data["yearID"], data["stint"]))
                result = cursor.fetchone()

                if result["count"] > 0:
                    flash("Duplicate entry detected: A record with the same Player ID, Year, and Stint already exists.", "danger")
                    return redirect(url_for("pitching_page"))

                # Add the new pitching record
                if Pitching.add_pitching(data):
                    flash("Successfully added a new record!", "success")
                else:
                    flash("Failed to add pitching data.", "danger")

        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            print(f"Error adding pitching data: {e}")
        finally:
            if connection:
                connection.close()

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
        success = Pitching.update_pitching(record_id=id, updated_data=updated_data)
        if success:
            flash("Data updated successfully!", "success")
        else:
            flash("Failed to update data.", "danger")

    return redirect(url_for('pitching_page'))