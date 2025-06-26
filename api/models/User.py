from datetime import datetime
import bcrypt


class UserModel:
    required_fields = {
        "first_name": "First name is required",
        "last_name": "Last name is required",
        "email": "Email is required",
        "password": "Password is required",
        "phone_number": "Phone number is required",
        "user_name": "Username is required"
    }

    def __init__(self, data):
        self.data = data  # Store raw data for validation

        self._id = data.get("_id")  # Optional for MongoDB usage
        self.first_name = data.get("first_name", "").strip()
        self.last_name = data.get("last_name", "").strip()
        self.email = data.get("email", "").strip()
        self.password = data.get("password", "")
        self.phone_number = data.get("phone_number", "").strip()
        self.user_name = data.get("user_name", "").strip()

        self.email_verified = data.get("email_verified", False)
        self.email_verified_at = data.get("email_verified_at")
        self.is_active = data.get("is_active", True)
        self.is_phone_number_verified = data.get("is_phone_number_verified", False)

        now = datetime.utcnow()
        self.created_at = data.get("created_at") or now
        self.updated_at = data.get("updated_at") or now
        self.deleted_at = data.get("deleted_at")

    def validate(self):
        errors = []
        for field, message in self.required_fields.items():
            value = self.data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(message)

        if errors:
            raise ValueError("; ".join(errors))

    def hash_password(self):
        if self.password:
            hashed = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt())
            self.password = hashed.decode("utf-8")

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "email_verified": self.email_verified,
            "email_verified_at": self.email_verified_at,
            "is_active": self.is_active,
            "phone_number": self.phone_number,
            "is_phone_number_verified": self.is_phone_number_verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "user_name": self.user_name
        }

    def to_json(self):
        return {
            "_id": str(self._id) if self._id else None,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "email_verified": self.email_verified,
            "email_verified_at": self.email_verified_at,
            "is_active": self.is_active,
            "phone_number": self.phone_number,
            "is_phone_number_verified": self.is_phone_number_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None if self.deleted_at else None,
            "user_name": self.user_name
        }

    def to_public_dict(self):
        data = self.to_dict()
        data.pop("password", None)
        return data
