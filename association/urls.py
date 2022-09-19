from django.urls import path
from .views import (
    CreateAssociation, 
    AssociationDetailView,

    CreateAssociationGroup,
    AssociationGroupDetailView,

    CreateAssociationMember,
    AssociationMemberDetailView,
)

urlpatterns = [
    path('', view=CreateAssociation.as_view(), name="create-association"),
    path('<int:pk>/', view=AssociationDetailView.as_view(),
         name="association-detail"),
    
    path('groups/', view=CreateAssociationGroup.as_view(),
         name="create-association-group"),
    path("groups/<int:pk>/", view=AssociationGroupDetailView.as_view(),
         name="associationgroup-detail"),
    
    path('members/', view=CreateAssociationMember.as_view(),
         name="create-association-member"),
    path("members/<int:pk>/", view=AssociationMemberDetailView.as_view(),
         name="associationmember-detail"),

]
