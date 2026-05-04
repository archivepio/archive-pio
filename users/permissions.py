from rest_framework.permissions import BasePermission

STAFF_ROLES = {'staff', 'admin', 'administrator', 'superadmin'}


class IsStaffOrAdmin(BasePermission):
    """Only allows staff or admin users to access the view."""
    message = 'You do not have permission to perform this action. Staff or Admin access required.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'role') and request.user.role:
            return request.user.role.role_name.lower() in STAFF_ROLES
        return False


class IsOwnerOrStaff(BasePermission):
    """
    - Staff/Admin: full access to any object.
    - Citizens: can only access their own objects (checked via has_object_permission).
    """
    message = 'You do not have permission to access this resource.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'role') and request.user.role:
            if request.user.role.role_name.lower() in STAFF_ROLES:
                return True
        # For citizen: check if the object belongs to them
        # Works for Request (requester.email == user.email)
        if hasattr(obj, 'requester'):
            return obj.requester.email == request.user.email
        # Works for Notification
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False
