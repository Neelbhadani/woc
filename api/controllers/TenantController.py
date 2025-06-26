from bson import ObjectId
from flask import request, jsonify
from api.extensions import mongo
from api.models import TenantModel  # ✅ Use direct model import
from api.services.TenantService import check_is_tenant  # Adjust import if needed


class TenantController:

    @staticmethod
    def create_tenant(current_user):
        raw_data = request.get_json()
        result = check_is_tenant(raw_data, current_user)

        if isinstance(result, tuple):
            return result  # e.g., (jsonify({...}), 400)
        if isinstance(result, dict):
            return jsonify({
                "message": "Tenant created successfully",
                "tenant": result
            }), 201
        return result  # fallback if it's already a Response object

    @staticmethod
    def get_tenants(tenant_id=None):
        try:
            if tenant_id:
                tenant_data = mongo.db.tenants.find_one({"_id": ObjectId(tenant_id)})
                if tenant_data:
                    return jsonify(TenantModel.serialize_tenant(tenant_data))
                return jsonify({"error": "Tenant not found"}), 404
            else:
                tenants = mongo.db.tenants.find()
                tenant_list = [TenantModel.serialize_tenant(t) for t in tenants]
                return jsonify(tenant_list)
        except Exception as e:
            return jsonify({"error": "Failed to retrieve tenants", "details": str(e)}), 500
