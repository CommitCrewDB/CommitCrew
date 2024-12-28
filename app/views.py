from flask import render_template, request, redirect, url_for, flash
from flask import app
from app.models.teams import Teams
from app.models.fielding import Fielding
from app.models.pitching import Pitching
from app.models.master import Master



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

def fielding_page():
    player_id = request.args.get("player_id", "")
    league = request.form.get("league")
    year = request.args.get("year", "")
    position = request.args.get("position", "")
    action = request.args.get("action")

    leagues = Teams.get_all_leagues()

    if league or player_id or year or position:
        fielding_records = Fielding.filter_fielding(
            leagues=league,
            player_id=player_id,
            year=year,
            position=position
        )
    else:
        fielding_records = []

    return render_template(
        "fielding.html",
        fielding_records=fielding_records,
        leagues=leagues,
        player_id=player_id,
        year=year,
        position=position,
    )



def pitching_options():
    return render_template("pitching_options.html")

def pitching_table():
    action = request.args.get('action', 'view_all')
    search_query = request.args.get('search', '')

    if action == 'view_all':
        pitching_data = Pitching.load_pitching_data()
        return render_template("pitching.html", pitching_data=pitching_data)

    elif action == 'search' and search_query:
        # Search for specific data
        pitching_data = Pitching.search_and_sort(search_query=search_query)
        return render_template("pitching.html", pitching_data=pitching_data, search_query=search_query)

    # Default behavior: return to pitching options
    return redirect(url_for('pitching_options'))

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
