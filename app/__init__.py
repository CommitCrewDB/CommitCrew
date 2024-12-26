from flask import Flask
import os
from app import views

def create_app():
    app = Flask(__name__, template_folder="templates")

    app.secret_key = os.getenv("SECRET_KEY", "your-default-secret-key")
    
    app.add_url_rule(rule="/", view_func=views.home_page)
    app.add_url_rule(rule="/teams", view_func=views.teams_page, methods=["GET", "POST"])
    app.add_url_rule(rule="/teams/add", view_func=views.add_team_page, methods=["GET", "POST"])
    app.add_url_rule(rule="/fielding", view_func=views.fielding_page)
    app.add_url_rule(rule="/about", view_func=views.about_page)
    app.add_url_rule(rule="/pitching-options/", view_func=views.pitching_options)
    app.add_url_rule(rule="/pitching", view_func=views.pitching_table)
    app.add_url_rule(rule="/master-options/", view_func=views.master_options)
    app.add_url_rule(rule="/master", view_func=views.master_table)

    return app
