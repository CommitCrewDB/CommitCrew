from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="templates")
    from app import views
    app.add_url_rule(rule="/", view_func=views.home_page)
    app.add_url_rule(rule="/teams", view_func=views.teams_page)
    app.add_url_rule(rule="/fielding", view_func=views.fielding_page)
    app.add_url_rule(rule="/pitching", view_func=views.pitching_page)
    app.add_url_rule(rule="/about", view_func=views.about_page)

    return app
