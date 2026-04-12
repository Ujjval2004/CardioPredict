import jwt
import os
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("JWT_SECRET_KEY")

def generate_token(user_id, role):

    payload = {
        "id": str(user_id),   # ensure string
        "role": role
    }

    token = jwt.encode(payload, SECRET, algorithm="HS256")

    return token


def token_required(role=None):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"error": "Token missing"}), 401

            try:
                token = auth_header.split(" ")[1]

                data = jwt.decode(
                    token,
                    SECRET,
                    algorithms=["HS256"]
                )

            except Exception as e:
                print("JWT ERROR:", e)
                return jsonify({"error": "Invalid token"}), 401

            if role and data.get("role") != role:
                return jsonify({"error": "Unauthorized"}), 403

            return f(data, *args, **kwargs)

        return wrapper

    return decorator