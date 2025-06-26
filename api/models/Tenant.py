from datetime import datetime
from bson import ObjectId
from flask import jsonify
from api.extensions import mongo  # Adjust this if needed


class TenantModel:
    required_fields = {
        "first_name": "First name is required",
        "last_name": "Last name is required",
    }

    def __init__(self, data):
        self.data = data  # raw data for validation

        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")

        self.user_id = ObjectId(data.get("user_id")) if data.get("user_id") else None
        self.created_by = ObjectId(data.get("created_by")) if data.get("created_by") else None
        self.updated_by = ObjectId(data.get("updated_by")) if data.get("updated_by") else None

        now = datetime.utcnow()
        self.created_at = data.get("created_at") or now
        self.updated_at = data.get("updated_at") or now

    def validate(self):
        errors = []
        for field, message in self.required_fields.items():
            value = self.data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(message)
        if errors:
            raise ValueError("; ".join(errors))

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_id": self.user_id,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self):
        return {
            "_id": str(self.data.get("_id")) if self.data.get("_id") else None,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_id": str(self.user_id) if self.user_id else None,
            "created_by": str(self.created_by) if self.created_by else None,
            "updated_by": str(self.updated_by) if self.updated_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def serialize_tenant(data):
        return {
            "id": str(data["_id"]),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "user_id": str(data.get("user_id")) if data.get("user_id") else None,
            "created_by": str(data.get("created_by")) if data.get("created_by") else None,
            "updated_by": str(data.get("updated_by")) if data.get("updated_by") else None,
            "created_at": data.get("created_at").isoformat() if data.get("created_at") else None,
            "updated_at": data.get("updated_at").isoformat() if data.get("updated_at") else None
        }
