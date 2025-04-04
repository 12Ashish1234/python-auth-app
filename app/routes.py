from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.auth import auth
from app.models import User

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return jsonify({"message": "Welcome to the Flask API!"})


@main.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify(
        [{"id": u.id, "username": u.username} for u in users]
    )


def init_routes(app):
    app.register_blueprint(main)
    app.register_blueprint(auth)
