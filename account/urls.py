from django.urls import path
from .views import (LeviesView, 
                    LevyDetailView,
                    LevyChargesView,
                    LevyChargesDetailView,
)

urlpatterns = [
    path('levies/', view=LeviesView.as_view(), name="levies"),
    path('levies/<int:pk>/', view=LevyDetailView.as_view(),
         name="levy-detail"),
    
    path('levies/<int:levyId>/charges/',
         view=LevyChargesView.as_view(), name="levycharges"),
    
    path('levies/<int:levyId>/charges/<int:pk>/', view=LevyChargesDetailView.as_view(),
         name="levycharge-detail"),
]
