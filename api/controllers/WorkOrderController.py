# app/controllers/WorkOrderController.py

from flask import request, jsonify
from pymongo.errors import PyMongoError
from api.extensions import mongo
from api.services.RoleService import assign_role
from api.models import UserModel


class WorkOrderController:

    @staticmethod
    def create_workOrder():
        try:
            data = request.get_json()

            if mongo.db.users.find_one({"email": data.get("email")}):
                return jsonify({"error": "Email already exists"}), 400

            if mongo.db.users.find_one({"user_name": data.get("user_name")}):
                return jsonify({"error": "Username already taken"}), 400

            user = UserModel(data)
            user.validate()
            user.hash_password()

            user_dict = user.to_dict()
            result = mongo.db.users.insert_one(user_dict)

            if not assign_role(data["role"], result.inserted_id):
                return jsonify({"error": "Invalid or unknown role"}), 400

            user_data = user.to_public_dict()
            user_data["_id"] = str(result.inserted_id)

            return jsonify({
                "message": "User registered successfully",
                "user": user_data
            }), 201

        except ValueError as ve:
            return jsonify({"error": "Validation error", "details": str(ve)}), 400
        except PyMongoError as e:
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500



    # @staticmethod
    # def get_users(user_id=None):
    #     pipeline = []
    #
    #     if user_id:
    #         try:
    #             pipeline.append({"$match": {"_id": ObjectId(user_id)}})
    #         except Exception:
    #             return jsonify({"error": "Invalid user ID format"}), 400
    #
    #     pipeline += [
    #         {"$lookup": {
    #             "from": "user_has_roles",
    #             "localField": "_id",
    #             "foreignField": "user_id",
    #             "as": "role_links"
    #         }},
    #         {"$unwind": {
    #             "path": "$role_links",
    #             "preserveNullAndEmptyArrays": True
    #         }},
    #         {"$lookup": {
    #             "from": "roles",
    #             "localField": "role_links.role_id",
    #             "foreignField": "_id",
    #             "as": "role"
    #         }},
    #         {"$unwind": {
    #             "path": "$role",
    #             "preserveNullAndEmptyArrays": True
    #         }},
    #         {"$lookup": {
    #             "from": "role_has_permissions",
    #             "localField": "role._id",
    #             "foreignField": "role_id",
    #             "as": "role_permission_links"
    #         }},
    #         {"$unwind": {
    #             "path": "$role_permission_links",
    #             "preserveNullAndEmptyArrays": True
    #         }},
    #         {"$lookup": {
    #             "from": "permissions",
    #             "localField": "role_permission_links.permission_id",
    #             "foreignField": "_id",
    #             "as": "permission"
    #         }},
    #         {"$unwind": {
    #             "path": "$permission",
    #             "preserveNullAndEmptyArrays": True
    #         }},
    #         {"$group": {
    #             "_id": {
    #                 "user_id": "$_id",
    #                 "role_id": "$role._id",
    #                 "role_name": "$role.name"
    #             },
    #             "email": {"$first": "$email"},
    #             "user_name": {"$first": "$user_name"},
    #             "permissions": {"$addToSet": "$permission.name"}
    #         }},
    #         {"$group": {
    #             "_id": "$_id.user_id",
    #             "email": {"$first": "$email"},
    #             "user_name": {"$first": "$user_name"},
    #             "roles": {
    #                 "$push": {
    #                     "name": "$_id.role_name",
    #                     "permissions": "$permissions"
    #                 }
    #             }
    #         }}
    #     ]
    #
    #     try:
    #         result = list(mongo.db.users.aggregate(pipeline))
    #         for user in result:
    #             user["_id"] = str(user["_id"])
    #         if user_id:
    #             return jsonify(result[0] if result else {"error": "User not found"}), (200 if result else 404)
    #         else:
    #             return jsonify(result)
    #     except Exception as e:
    #         return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500
