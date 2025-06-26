from datetime import datetime
from bson import ObjectId


class TenantToPropertyModel:
    required_fields = {
        "property_id": "Property ID is required",
        "tenant_id": "Tenant ID is required",
    }

    def __init__(self, data):
        self.data = data

        self._id = data.get("_id")
        self.property_id = ObjectId(data.get("property_id")) if data.get("property_id") else None
        self.tenant_id = ObjectId(data.get("tenant_id")) if data.get("tenant_id") else None
        self.status = data.get("status", "active")  # Default to "active"

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
            "property_id": self.property_id,
            "tenant_id": self.tenant_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self):
        return {
            "_id": str(self._id) if self._id else None,
            "property_id": str(self.property_id) if self.property_id else None,
            "tenant_id": str(self.tenant_id) if self.tenant_id else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def serialize(data):
        return {
            "id": str(data.get("_id")) if data.get("_id") else None,
            "property_id": str(data.get("property_id")) if data.get("property_id") else None,
            "tenant_id": str(data.get("tenant_id")) if data.get("tenant_id") else None,
            "status": data.get("status"),
            "created_at": data.get("created_at").isoformat() if data.get("created_at") else None,
            "updated_at": data.get("updated_at").isoformat() if data.get("updated_at") else None
        }
