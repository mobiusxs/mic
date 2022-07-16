from flask import Flask

from mic import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    return app


def register_extensions(app):
    from mic.extensions import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    from mic.admin.views import admin
    from mic.auth.views import auth
    from mic.dashboard.views import dashboard

    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)


def register_shellcontext(app):
    from mic.extensions import db

    def shell_context():
        return {
            "db": db,
        }

    app.shell_context_processor(shell_context)
