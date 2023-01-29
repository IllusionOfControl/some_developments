from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    from app.views import views

    app.register_blueprint(views)

    db.init_app(app)
    db.create_all(app=app)

    return app
