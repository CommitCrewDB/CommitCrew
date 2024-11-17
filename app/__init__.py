from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home_page():
        return "Welcome to the website for the Baseball History!"

    return app