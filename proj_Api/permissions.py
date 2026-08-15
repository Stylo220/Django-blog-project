from rest_framework.permissions import BasePermission, SAFE_METHODS



class PostListDetailPermission(BasePermission):
    """
    for retrieving article list, any user can see
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return False



class UserEditPermission(BasePermission):
    """
    for altering user objects, only superuser and staff with their own objects can alter
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and obj == request.user:
            return True
        if request.user.is_staff and request.method in SAFE_METHODS:
            return True
        return False

class UserListPermission(BasePermission):
    """
    for retrieving user list, only superuser and staff can see
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS :
            return True
        return False

class TicketPermission(BasePermission):
    """
    for creating tickets, any user can create
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return False