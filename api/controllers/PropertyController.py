from bson import ObjectId
from flask import jsonify, request
from pymongo.errors import PyMongoError

from api.extensions import mongo
from api.models import PropertyModel  # Adjust path as needed


class PropertyController:

    @staticmethod
    def get_property(property_id=None):
        try:
            if property_id:
                property_data = mongo.db.properties.find_one({"_id": ObjectId(property_id)})
                if property_data:
                    return jsonify(PropertyModel.serialize_property(property_data))
                else:
                    return jsonify({"error": "Property not found"}), 404
            else:
                property_data = mongo.db.properties.find()
                property_list = [PropertyModel.serialize_property(prop) for prop in property_data]
                return jsonify(property_list)
        except Exception as e:
            return jsonify({"error": "Failed to retrieve property", "details": str(e)}), 500

    @staticmethod
    def create_property(current_user):
        try:
            raw_data = request.get_json()
            raw_data["created_by"] = current_user["_id"]
            raw_data["updated_by"] = current_user["_id"]

            property_model = PropertyModel(raw_data)
            property_model.validate()

            result = mongo.db.properties.insert_one(property_model.to_dict())
            property_model._id = result.inserted_id

            return jsonify({
                "message": "Property created",
                "property": property_model.to_json()
            }), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except PyMongoError as e:
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
