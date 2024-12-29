from flask import Flask
import os
from app import views

def create_app():
    app = Flask(__name__, template_folder="templates")

    app.secret_key = os.getenv("SECRET_KEY", "your-default-secret-key")
    
    app.add_url_rule(rule="/", view_func=views.home_page)
    app.add_url_rule(rule="/teams", view_func=views.teams_page, methods=["GET", "POST"])
    app.add_url_rule(rule="/teams/add", view_func=views.add_team_page, methods=["GET", "POST"])
    app.add_url_rule(rule="/teams/update/<int:team_id>", view_func=views.update_team_page, methods=["GET", "POST"])
    app.add_url_rule(rule="/teams/delete/<int:team_id>", view_func=views.delete_team, methods=["POST"])
    app.add_url_rule(rule="/fielding", view_func=views.fielding_page, methods=["GET", "POST"])
    app.add_url_rule(rule="/fielding/add", view_func=views.add_fielding_page, methods=["GET", "POST"])
    app.add_url_rule(rule="/fielding/update/<int:record_id>", view_func=views.update_fielding_page, methods=["GET", "POST"])
    app.add_url_rule(rule="/fielding/delete/<int:record_id>", view_func=views.delete_fielding_record, methods=["POST"])
    app.add_url_rule(rule="/about", view_func=views.about_page)
    app.add_url_rule(rule="/pitching/add", view_func=views.add_pitching_data, methods= ["GET", "POST"])
    app.add_url_rule(rule="/pitching", view_func=views.pitching_page)
    app.add_url_rule(rule="/pitching/update/<int:id>", view_func=views.update_pitching_data, methods=["GET", "POST"])
    app.add_url_rule(rule="/pitching/delete/<int:id>", view_func=views.delete_pitching_data, methods=["GET"])
    app.add_url_rule(rule="/batting", view_func=views.batting_page)
    app.add_url_rule(rule="/batting/add", view_func=views.add_batting_record, methods=["GET", "POST"])
    app.add_url_rule(rule="/batting/update/<int:record_id>", view_func=views.update_batting_record, methods=["GET", "POST"])
    app.add_url_rule(rule="/batting/delete/<int:record_id>", view_func=views.delete_batting_record, methods=["POST"])
    app.add_url_rule(rule="/master-options/", view_func=views.master_options)
    app.add_url_rule(rule="/master", view_func=views.master_table)

    return app
