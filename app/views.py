from flask import render_template
from app.models.teams import Teams



def home_page():
    return render_template("home.html")

def teams_page():
    teams = Teams.get_all_teams()
    return render_template("teams.html", teams=teams)

def fielding_page():
    return render_template("fielding.html")

def pitching_page():
    return render_template("pitching.html")

def about_page():
    return render_template("about.html")