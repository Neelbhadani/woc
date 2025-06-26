from flask import jsonify, request
from bson import ObjectId
from pymongo.errors import PyMongoError
from api.extensions import mongo
from api.models import RoleModel


class RoleController:

    @staticmethod
    def get_roles(role_id=None):
        try:
            if role_id:
                role = mongo.db.roles.find_one({"_id": ObjectId(role_id)})
                if role:
                    return jsonify(RoleModel.serialize_role(role))
                else:
                    return jsonify({"error": "Role not found"}), 404
            else:
                roles = mongo.db.roles.find()
                role_list = [RoleModel.serialize_role(role) for role in roles]
                return jsonify(role_list)
        except Exception as e:
            return jsonify({"error": "Failed to fetch role(s)", "details": str(e)}), 500

    @staticmethod
    def create_role(current_user=None):  # `current_user` is not used, can be omitted
        try:
            data = request.get_json()

            if mongo.db.roles.find_one({"name": data.get("name")}):
                return jsonify({"error": "Role already exists"}), 400

            role = RoleModel(data)
            role.validate()

            result = mongo.db.roles.insert_one(role.to_dict())
            role._id = result.inserted_id

            return jsonify({
                "message": "Role added successfully",
                "role": role.to_json()
            }), 201

        except ValueError as ve:
            return jsonify({"error": "Validation error", "details": str(ve)}), 400
        except PyMongoError as e:
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
