from flask import Flask
from flask_jwt_extended import JWTManager

from app.models import db
from app.routes import init_routes

jwt = JWTManager()


def create_app(testing=False):
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config.from_object("config.Config")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    # Initialize plugins
    db.init_app(app)
    jwt.init_app(app)

    # Create database tables within app context
    with app.app_context():
        db.create_all()

    init_routes(app)
    return app
