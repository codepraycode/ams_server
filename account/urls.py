from django.urls import path
from .views import AssociationAccount

urlpatterns = [
    path('', view=AssociationAccount.as_view(), name="account"),
]
