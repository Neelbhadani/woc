from flask import jsonify
from bson import ObjectId
from api.extensions import mongo
from api.models import TenantModel, UserModel
from api.services.RoleService import assign_role


def check_is_tenant(data, current_user=None):
    try:
        user_data = mongo.db.users.find_one({"email": data["email"]})
        if user_data:
            tenant_data = mongo.db.tenants.find_one({"user_id": user_data["_id"]})
            if tenant_data:
                return {
                    "message": "Tenant already exists",
                    "tenant": TenantModel.serialize_tenant(tenant_data)
                }
            return create_tenant(user_data, current_user)

        # User does not exist, create new user
        user = UserModel(data)
        user.validate()
        user.hash_password()

        user_dict = user.to_dict()
        result = mongo.db.users.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id

        assign_role("T", result.inserted_id)
        return create_tenant(user_dict, current_user)

    except ValueError as ve:
        return jsonify({"error": "Validation error", "details": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to check or create tenant", "details": str(e)}), 500


def create_tenant(user_data, current_user):
    try:
        user_id = ObjectId(user_data["_id"])
        if mongo.db.tenants.find_one({"user_id": user_id}):
            return {
                "message": "Tenant already exists",
                "tenant": TenantModel.serialize_tenant(mongo.db.tenants.find_one({"user_id": user_id}))
            }

        tenant_payload = {
            "user_id": user_id,
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "created_by": ObjectId(current_user["_id"]) if current_user else None,
            "updated_by": ObjectId(current_user["_id"]) if current_user else None,
        }

        tenant_model = TenantModel(tenant_payload)
        tenant_model.validate()

        result = mongo.db.tenants.insert_one(tenant_model.to_dict())
        tenant_model.data["_id"] = result.inserted_id

        return tenant_model.to_json()

    except ValueError as ve:
        raise Exception(str(ve))
    except Exception as e:
        raise Exception(f"Internal server error: {str(e)}")

