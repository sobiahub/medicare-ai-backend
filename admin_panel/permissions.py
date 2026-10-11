from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):

    message = "Admin access is required."

    def has_permission(self, request, view):

        user = getattr(request, "user", None)

        if not user:
            return False

        return user.get("role") == "admin"