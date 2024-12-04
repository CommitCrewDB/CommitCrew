from flask import render_template
from app.models.teams import Teams
from app.models.fielding import Fielding


def home_page():
    return render_template("home.html")

def teams_page():
    teams = Teams.get_all_teams()
    return render_template("teams.html", teams=teams)

def fielding_page():
    fielding_records = Fielding.get_all_fielding()
    return render_template("fielding.html",fielding_records = fielding_records)

def pitching_page():
    return render_template("pitching.html")

def about_page():
    return render_template("about.html")

def master_page():
    return render_template("master.html")
