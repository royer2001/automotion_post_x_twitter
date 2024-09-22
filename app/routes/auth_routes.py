from flask import Blueprint, request, jsonify
from ..models.user import User
from .. import db
from app import bcrypt, jwt
from flask_jwt_extended import create_access_token
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Obtener la fecha y hora actual
        now = datetime.now()

        # Calcular el tiempo hasta las 23:59:59 del día actual
        expiration_time = datetime(now.year, now.month, now.day, 23, 59, 59)
        expires_delta = expiration_time - now

        # Crear el token con una expiración personalizada
        access_token = create_access_token(identity={'username': user.username}, expires_delta=expires_delta)

        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid credentials"}), 401
