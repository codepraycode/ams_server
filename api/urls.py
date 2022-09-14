from django.urls import path
from .views import ObtainAssociationAuthToken

urlpatterns = [
    path('auth/', view=ObtainAssociationAuthToken.as_view(), name="association_auth"),
]
