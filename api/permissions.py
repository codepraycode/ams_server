
from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.association and request.association.is_active)
    
    def has_object_permission(self, request, view, obj):
        if request.association.pk is not obj.pk:
            return False
        
        return super().has_object_permission(request, view, obj) 
