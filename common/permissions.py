from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.

    # Point 7: Role-based access control
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role == "ADMIN"
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Admins can do anything.
    Others can only read.

    # Point 7
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role == "ADMIN"
        )


class IsOrderOwner(BasePermission):
    """
    Object-level permission.
    Only the owner of the order or admin can access it.

    # Point 7
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.role == "ADMIN":
            return True

        # obj.user is assumed to be the order owner
        return obj.user == user
