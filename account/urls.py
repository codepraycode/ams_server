from django.urls import path
from .views import (LeviesView, 
                    LevyDetailView,
                    LevyChargesView,
                    LevyChargesDetailView,
                    LevyChargeMembersView,
                    MemberPaymentView,
                    MemberPaymentTransactionsView
)

urlpatterns = [
    path('levies/', view=LeviesView.as_view(), name="levies"),
    path('levies/<int:pk>/', view=LevyDetailView.as_view(),
         name="levy-detail"),
    
    path('levies/charges/create/',
         view=LevyChargesView.as_view(), 
         name="levycharges"
     ),
         
    path('levies/charges/<int:pk>/', view=LevyChargesDetailView.as_view(),
         name="levycharge-detail"),


    path('levies/charges/<int:chargePk>/members/', view=LevyChargeMembersView.as_view(),
         name="levychargemembers-detail"),
    
    path('levies/charges/payment/', view=MemberPaymentView.as_view(),
         name="levycharge-payment"),
    
    path('member/topup/', view=MemberPaymentView.as_view(),
         name="member-topup"),
    
    path('member/<int:accountPk>/transactions/', view=MemberPaymentTransactionsView.as_view(),
         name="member-account-transactions"), # GET
]
