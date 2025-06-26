from flask import Blueprint
from api.controllers import UserController,TenantController,PropertyController,RoleController

from api.Middleware import token_required

user_bp = Blueprint("user_bp", __name__)

# --------------------
# Auth Routes
# --------------------

@user_bp.route('/register', methods=['POST'])
def register():
    return UserController.register_user()

@user_bp.route('/login', methods=['POST'])
def login():
    return UserController.user_login()

@user_bp.route("/logout", methods=["POST"])
@token_required
def logout(current_user):
    return UserController.logout_user(current_user)

# --------------------
# User Routes
# --------------------

@user_bp.route("/users", methods=["GET"])
@user_bp.route("/users/<user_id>", methods=["GET"])
@token_required
def users(current_user, user_id=None):
    return UserController.get_users(user_id)

# --------------------
# Property Routes
# --------------------

@user_bp.route("/properties", methods=["POST"])
@token_required
def create_property(current_user):
    return PropertyController.create_property(current_user)

@user_bp.route("/property", methods=["GET"])
@user_bp.route("/property/<property_id>", methods=["GET"])
@token_required
def get_property(current_user, property_id=None):
    return PropertyController.get_property(property_id)

# --------------------
# Role Routes
# --------------------

@user_bp.route("/roles", methods=["POST"])
@token_required
def create_role(current_user):
    return RoleController.create_role(current_user)

@user_bp.route("/roles", methods=["GET"])
@user_bp.route("/roles/<role_id>", methods=["GET"])
@token_required
def get_roles(current_user, role_id=None):
    return RoleController.get_roles(role_id)

# --------------------
# Tenant Routes
# --------------------

@user_bp.route("/tenants", methods=["POST"])
@token_required
def create_tenant(current_user):
    return TenantController.create_tenant(current_user)

@user_bp.route("/tenants", methods=["GET"])
@user_bp.route("/tenants/<tenant_id>", methods=["GET"])
@token_required
def get_tenants(current_user, tenant_id=None):
    return TenantController.get_tenants(tenant_id)
