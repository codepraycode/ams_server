from django.urls import path
from .views import CreateAssociation, AssociationView

urlpatterns = [
    path('<int:pk>/', view=AssociationView.as_view(), name="rud_association"),
    path('', view=CreateAssociation.as_view(), name="create_association"),
]
