from flask import render_template, request
from app.models.teams import Teams
from app.models.fielding import Fielding

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

def pitching_page():
    return render_template("pitching.html")

def about_page():
    return render_template("about.html")

def master_page():
    return render_template("master.html")

