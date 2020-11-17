from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from backblaze import BackblazeFileUploader
from flask_migrate import Migrate
import os


db = SQLAlchemy()
migrate = Migrate()

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_config(app):    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["database_uri"] 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 300


def create_app():
    app = Flask(__name__)
    with app.app_context():
        register_config(app)
        register_extensions(app)

        g.backblaze = BackblazeFileUploader()
        
        import models
        import routes

    return app
