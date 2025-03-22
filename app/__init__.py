from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.routes import init_routes
from app.models import db  # Ensure you import db from models

jwt = JWTManager()


def create_app(testing=False):
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config.from_object("config.Config")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///:memory:"  # Use an in-memory DB for tests
    )
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing if necessary

    # Initialize plugins
    db.init_app(app)
    jwt.init_app(app)

    # Create database tables within app context
    with app.app_context():
        db.create_all()  # Ensure the database is initialized

    init_routes(app)
    return app
