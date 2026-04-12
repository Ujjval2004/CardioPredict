from flask import Blueprint, request, jsonify
from models import db, User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# ================= REGISTER =================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print("Received registration data:", data)

    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    name = data.get("name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not username or not email or not password or not role:
        return jsonify({"error": "All required fields must be provided"}), 400

    try:
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already taken"}), 400

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()
        print("User Saved",new_user.id)

        return jsonify({"message": "User registered successfully"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ================= LOGIN =================
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password"}), 401

    # IMPORTANT: identity must be string
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    }), 200