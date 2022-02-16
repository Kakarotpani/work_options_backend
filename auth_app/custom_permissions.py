from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_client:
            return True
        else:
            return False

class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_freelancer:
            return True
        else:
            return False