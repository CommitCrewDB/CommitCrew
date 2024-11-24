from flask import render_template


def home_page():
    return render_template("home.html")

def movies_page():
    return render_template("teams.html")

def fielding_page():
    return render_template("fielding.html")
