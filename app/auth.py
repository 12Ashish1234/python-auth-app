from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

from app.models import User, db

bcrypt = Bcrypt()
auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = (
        bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    )
    user = User(username=data["username"], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        token = create_access_token(identity=user.username)
        return jsonify({"token": token})
    return jsonify({"message": "Invalid credentials"}), 401
