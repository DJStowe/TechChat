from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import User

# Authenticated have read access. Staff members have write access.
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        else:
            return request.user and request.user.is_staff

class TechChatIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return 'techchat_userid' in request.session

class TechChatIsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if 'techchat_userid' in request.session:
            if request.method in SAFE_METHODS:
                return True
            else:
                userid = request.session.get('techchat_userid')
                user   = User.objects.get(id=userid)
                return user.is_staff
        else:
            return False
