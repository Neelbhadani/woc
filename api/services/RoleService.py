from api.extensions import mongo
from bson import ObjectId

def assign_role(role, user_id):
    role_map = {
        "A": "admin",
        "M": "manager",
        "AA": "Admin Assist",
        "C": "contractor",
        "T": "tenant",
        "O": "owner"
    }

    role_name = role_map.get(role)
    if not role_name:
        return {"error": f"Unknown role code '{role}'"}

    role_data = mongo.db.roles.find_one({"name": role_name})
    if not role_data:
        return {"error": f"Role '{role_name}' not found in the database."}

    try:
        user_obj_id = ObjectId(user_id) if isinstance(user_id, str) else user_id

        # Assign the role
        mongo.db.user_has_roles.insert_one({
            "user_id": user_obj_id,
            "role_id": role_data["_id"]
        })

        # Fetch the user
        user = mongo.db.users.find_one({"_id": user_obj_id})
        if user:
            user["_id"] = str(user["_id"])  # convert for JSON-safe output

        return {
            "message": f"Role '{role_name}' assigned successfully.",
            "user": user,
            "assigned_role": role_name
        }

    except Exception as e:
        return {"error": f"Error assigning role: {str(e)}"}
