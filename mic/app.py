from flask import Flask


def create_app():
    app = Flask(__name__)

    register_blueprints(app)
    return app


def register_blueprints(app):
    from mic.auth.views import auth
    from mic.dashboard.views import dashboard

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
