from datetime import datetime
from bson import ObjectId


class PropertyModel:
    required_fields = {
        "address": "Address is required",
        "city": "City is required",
        "state": "State is required",
        "country": "Country is required",
        "zip": "Zip code is required",
    }

    def __init__(self, data):
        self.data = data  # Raw input for validation

        self._id = data.get("_id")  # For MongoDB _id usage
        self.address = data.get("address")
        self.city = data.get("city")
        self.state = data.get("state")
        self.country = data.get("country")
        self.zip = data.get("zip")

        self.created_by = ObjectId(data.get("created_by")) if data.get("created_by") else None
        self.updated_by = ObjectId(data.get("updated_by")) if data.get("updated_by") else None

        now = datetime.utcnow()
        self.created_at = data.get("created_at") or now
        self.updated_at = data.get("updated_at") or now

    def validate(self):
        errors = []
        for field, error_msg in self.required_fields.items():
            value = self.data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(error_msg)

        if errors:
            raise ValueError("; ".join(errors))

    def to_dict(self):
        return {
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "zip": self.zip,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_json(self):
        return {
            "_id": str(self._id) if self._id else None,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "zip": self.zip,
            "created_by": str(self.created_by) if self.created_by else None,
            "updated_by": str(self.updated_by) if self.updated_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def serialize_property(data):
        return {
            "id": str(data["_id"]),
            "address": data.get("address"),
            "city": data.get("city"),
            "state": data.get("state"),
            "country": data.get("country"),
            "zip": data.get("zip"),
            "created_by": str(data.get("created_by")) if data.get("created_by") else None,
            "updated_by": str(data.get("updated_by")) if data.get("updated_by") else None,
            "created_at": data.get("created_at").isoformat() if data.get("created_at") else None,
            "updated_at": data.get("updated_at").isoformat() if data.get("updated_at") else None
        }
