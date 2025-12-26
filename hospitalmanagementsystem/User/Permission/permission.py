# permissions.py
from functools import wraps
from django.core.exceptions import PermissionDenied

def require_roles(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'current_user') or not self.current_user:
                raise PermissionDenied("Authentication required.")
            user_role = self.current_user.role.role_name.lower()
            if user_role not in [role.lower() for role in allowed_roles]:
                raise PermissionDenied(f"{', '.join(allowed_roles)} role(s) required.")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
