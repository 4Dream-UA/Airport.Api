from rest_framework.permissions import BasePermission

class IsNotAuthenticated(BasePermission):
    """
    Access only for no authenticated users.
    """
    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated
