from django.urls import path
from .views import (LeviesView, 
                    LevyDetailView,
                    LevyChargesView,
                    LevyChargesDetailView,
                    LevyChargeMembersView,
                    MemberPaymentView,
)

urlpatterns = [
    path('levies/', view=LeviesView.as_view(), name="levies"),
    path('levies/<int:pk>/', view=LevyDetailView.as_view(),
         name="levy-detail"),
    
    path('levies/<int:levyId>/charges/',
         view=LevyChargesView.as_view(), name="levycharges"),
    path('levies/<int:levyId>/charges/<int:pk>/', view=LevyChargesDetailView.as_view(),
         name="levycharge-detail"),


    path('levies/<int:levyId>/charges/<int:chargeId>/members/', view=LevyChargeMembersView.as_view(),
         name="levychargemembers-detail"),
    
    path('levies/<int:levyId>/charges/<int:chargeId>/payment/', view=MemberPaymentView.as_view(),
         name="levycharge-payment"),
    
    path('member/topup/', view=MemberPaymentView.as_view(),
         name="member-topup"),
]
