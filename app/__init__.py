from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.routes import init_routes
from app.models import db  # Ensure you import db from models

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize plugins
    db.init_app(app)
    jwt.init_app(app)

    # Create database tables within app context
    with app.app_context():
        db.create_all()  # Ensure the database is initialized

    init_routes(app)
    return app
