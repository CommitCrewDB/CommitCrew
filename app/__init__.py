from flask import Flask

import views

def create_app():
    app = Flask(__name__)
    app.add_url_rule(rule="/", view_func=views.home_page)
    app.add_url_rule(rule="/teams", view_func=views.teams_page)

    return app