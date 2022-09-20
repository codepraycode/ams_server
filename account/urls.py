from django.urls import path
from .views import LeviesView, LevyDetailView

urlpatterns = [
    path('levies/', view=LeviesView.as_view(), name="levies"),
    path('levies/<int:pk>/', view=LevyDetailView.as_view(),
         name="levy-detail"),
]
