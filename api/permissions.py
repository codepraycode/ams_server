
from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated association.
    """

    def has_permission(self, request, view):
        try:
            return bool(request.association and request.association.is_active)
        except:
            return False

class IsAssociation(BasePermission):
    """
    Allows access only rightful association.
    """

    def has_object_permission(self, request, view, obj):

        try:
            if request.association.pk is not obj.pk:
                return False
        except:
            return False

        return super().has_object_permission(request, view, obj) 


class IsAssociationGroup(BasePermission):
    """
    Allows access only rightful association.
    """

    def has_object_permission(self, request, view, obj):

        try:
            if request.association.pk is not obj.association.pk:
                return False
        except:
            return False

        return super().has_object_permission(request, view, obj) 


class IsAssociationMember(BasePermission):
    """
    Allows access only rightful association.
    """

    def has_object_permission(self, request, view, obj):
        
        try:
            if request.association.pk is not obj.member_group.association.pk:
                return False
        except:
            return False

        
        return super().has_object_permission(request, view, obj) 


class IsAssociationLevy(BasePermission):
    """
    Allows access only rightful association.
    """

    def has_object_permission(self, request, view, obj):
        
        try:
            if request.association.pk is not obj.association.pk:
                return False
        except:
            return False

        
        return super().has_object_permission(request, view, obj) 


class IsAssociationLevyCharge(BasePermission):
    """
    Allows access only rightful association.
    """

    def has_object_permission(self, request, view, obj):
        
        try:
            if request.association.pk is not obj.levy.association.pk:
                return False
        except:
            return False

        
        return super().has_object_permission(request, view, obj) 
