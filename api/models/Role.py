from datetime import datetime


class RoleModel:
    required_fields = {
        "name": "Role name is required",
    }

    def __init__(self, data):
        self.data = data

        self._id = data.get("_id")
        self.name = data.get("name", "").strip()

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
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def to_json(self):
        return {
            "_id": str(self._id) if self._id else None,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def serialize_role(data):
        return {
            "id": str(data["_id"]),
            "name": data.get("name"),
            "created_at": data.get("created_at").isoformat() if data.get("created_at") else None,
            "updated_at": data.get("updated_at").isoformat() if data.get("updated_at") else None
        }
