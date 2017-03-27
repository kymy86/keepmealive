from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        """
        Allow only to super_admin users
        """
        return request.user and request.user.is_superuser