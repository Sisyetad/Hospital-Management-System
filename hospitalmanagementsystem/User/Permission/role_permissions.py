# User/Permissions/role_permissions.py

from rest_framework.permissions import BasePermission
from .permission_config import ROLE_PERMISSIONS

class DynamicRolePermission(BasePermission):
    def has_permission(self, request, view):
        view_name = view.__class__.__name__
        action = getattr(view, 'action', None)
        key = f"{view_name}:{action}"
        allowed_roles = ROLE_PERMISSIONS.get(key, [])
        if "authenticated" in allowed_roles:
            return True
        user_role = getattr(request.user.role, 'role_name', None)
        return user_role in allowed_roles
