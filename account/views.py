from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status

# Mixins
# from rest_framework.mixins import ListModelMixin
# Parsers
from rest_framework.parsers import (MultiPartParser, FormParser, JSONParser)

# Permissions
from api.permissions import (IsAuthenticated, IsAssociationLevy, IsAssociationLevyCharge)

# Serializers
from .serializers import (LevySerializer, 
                        LevyChargeSerializer,
                        CreateAssociationMemberPaymentSerializer,
                        AssociationMemberPaymentSerializer,
                    )

# Models
from .models import (
    AssociationLevy, 
    AssociationLevyCharge, 
    AssociationMemberTransaction
)

from account.models import (
    AssociationMemeber,
    AssociationMemberAccount
)

# Create your views here.
class LeviesView(ListCreateAPIView):
    # Create and list levies
    serializer_class = LevySerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated, IsAssociationLevy,)


class LevyDetailView(RetrieveUpdateAPIView):
    serializer_class = LevySerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated, IsAssociationLevy,)
    queryset = AssociationLevy.objects.all()


# Charges view
class LevyChargesView(CreateAPIView):
    # Create a levy charge and return charge json data
    serializer_class = LevyChargeSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated, IsAssociationLevyCharge,)
    queryset = AssociationLevyCharge.objects.all()


class LevyChargesDetailView(RetrieveUpdateAPIView):
    serializer_class = LevyChargeSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated, IsAssociationLevyCharge,)
    queryset = AssociationLevyCharge.objects.all()



# Member transaction view
class MemberPaymentView(CreateAPIView):
    # Cover levy paryment, and account topup
    
    # Create and list levies
    serializer_class = CreateAssociationMemberPaymentSerializer
    # parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated,)
    queryset = AssociationMemberTransaction.objects.all()


class LevyChargeMembersView(ListAPIView):
    # Create and list levies
    serializer_class = AssociationMemberPaymentSerializer
    # parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated,)
    queryset = AssociationMemeber.objects.all()

    def list(self, request, *args, **kwargs):
        # get members in authenticated association
        # the idea is to get all the members in association that is connected
        # to the levy charge.
        
        # A member is connect if the member joined date is 
        #   later than the charge creation date.

        # grab the chargePk
        chargePk = kwargs.get('chargePk', None)

        # if no charge_id (which should be impossible), err!
        if not chargePk:
            return Response({"message":"Charge not given"}, status=status.HTTP_400_BAD_REQUEST)
        
        # try to get the charge from chargePk, err if not found
        try:
            charge = AssociationLevyCharge.objects.get(
                pk=chargePk, 
                levy__association=request.association
            )
        except AssociationLevyCharge.DoesNotExist as err:
            return Response({"message": "Charge not found"}, status=status.HTTP_404_NOT_FOUND)

        # load all payments associated with charge
        # charge is sure to be associated with the authenticated association
        # so all operation now is specific to authenticated association
        # payments_associated_with_charge = AssociationMemberTransaction.objects.filter(
        #     charge=charge)
        
        charged_members_accounts_queryset = AssociationMemberAccount.get_charge_members_account(charge)

        serializer = self.get_serializer(
            charged_members_accounts_queryset, many=True)
        return Response(serializer.data)

