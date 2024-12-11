from flask import render_template, request, redirect, url_for
from flask import app
from app.models.teams import Teams
from app.models.fielding import Fielding
from app.models.pitching import Pitching



def home_page():
    return render_template("home.html")

def teams_page():

    search_query = request.args.get("search", "")
    if search_query:
        teams = Teams.search_by_name(search_query)
    else:
        teams = []
    top_teams = Teams.get_top_teams_by_league()
    return render_template("teams.html", teams=teams, top_teams=top_teams)

def fielding_page():

    position_query = request.args.get("position", "")
    if position_query:
        fielding_records = Fielding.search_by_position(position_query)
    else:
        fielding_records = Fielding.get_all_fielding()
    return render_template("fielding.html", fielding_records=fielding_records)

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


def about_page():
    return render_template("about.html")

def master_page():
    return render_template("master.html")
