from flask import render_template


def home_page():
    return render_template("home.html")

def teams_page():
    return render_template("teams.html")

def fielding_page():
    return render_template("fielding.html")

def pitching_page():
    return render_template("pitching.html")

def about_page():
    return render_template("about.html")