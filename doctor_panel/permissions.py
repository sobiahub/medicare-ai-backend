from rest_framework.permissions import BasePermission


class IsDoctorUser(BasePermission):

    def has_permission(self, request, view):

        if not request.user:
            return False

        return (
            request.user.get("role") == "doctor"
            and request.user.get("is_active", True)
        )