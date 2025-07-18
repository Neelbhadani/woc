from functools import wraps
from flask import request, jsonify, current_app
import jwt
from bson import ObjectId
from api.extensions import mongo


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            # ❗ Check if token is blacklisted
            if mongo.db.blacklisted_tokens.find_one({"token": token}):
                return jsonify({"error": "Token has been revoked"}), 401

            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['u']
            current_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

            if not current_user:
                return jsonify({"error": "User not found"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"error": "Token validation failed", "details": str(e)}), 500

        return f(current_user, *args, **kwargs)

    return decorated
