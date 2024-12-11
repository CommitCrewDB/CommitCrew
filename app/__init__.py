from flask import Flask
from app import views

def create_app():
    app = Flask(__name__, template_folder="templates")
    
    app.add_url_rule(rule="/", view_func=views.home_page)
    app.add_url_rule(rule="/teams", view_func=views.teams_page)
    app.add_url_rule(rule="/fielding", view_func=views.fielding_page)
    app.add_url_rule(rule="/about", view_func=views.about_page)
    app.add_url_rule(rule="/pitching-options/", view_func=views.pitching_options)
    app.add_url_rule(rule="/pitching", view_func=views.pitching_table)
    return app
