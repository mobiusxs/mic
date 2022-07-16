from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123'

    register_blueprints(app)
    return app


def register_blueprints(app):
    from mic.admin.views import admin
    from mic.auth.views import auth
    from mic.dashboard.views import dashboard

    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
