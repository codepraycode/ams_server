from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status

# Mixins
from rest_framework.mixins import ListModelMixin
# Parsers
from rest_framework.parsers import (MultiPartParser, FormParser, JSONParser)

# Permissions
from api.permissions import (IsAuthenticated, IsAssociationLevy, IsAssociationLevyCharge)

# Serializers
from .serializers import (LevySerializer, 
                        LevyChargeSerializer,
                        CreateAssociationPaymentSerializer,
                        AssociationMemberPaymentSerializer,
                    )

# Models
from .models import (
    AssociationLevy, AssociationLevyCharge, AssociationPayment)
from account.models import AssociationMemeber

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


class LevyChargesView(ListCreateAPIView):
    # Create and list levies
    serializer_class = LevyChargeSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated, IsAssociationLevyCharge,)
    queryset = AssociationLevyCharge.objects.all()


class LevyChargesDetailView(RetrieveUpdateAPIView):
    serializer_class = LevyChargeSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated, IsAssociationLevyCharge,)
    queryset = AssociationLevyCharge.objects.all()


class LevyChargePaymentView(CreateAPIView):
    # Create and list levies
    serializer_class = CreateAssociationPaymentSerializer
    # parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated,)
    queryset = AssociationPayment.objects.all()


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

        # grab the chargeId
        chargeId = kwargs.get('chargeId', None)

        # if no charge_id (which should be impossible), err!
        if not chargeId:
            return Response({"message":"Charge id not given"}, status=status.HTTP_400_BAD_REQUEST)
        
        # try to get the charge from chargeId, err if not found
        try:
            charge = AssociationLevyCharge.objects.get(
                pk=chargeId, 
                levy__association=request.association
            )
        except AssociationLevyCharge.DoesNotExist as err:
            return Response({"message": "Charge not found"}, status=status.HTTP_404_NOT_FOUND)

        # load all payments associated with charge
        payments_associated_with_charge = AssociationPayment.objects.filter(charge=charge)
        
        # At this point, all is set for operation
        # queryset = self.get_queryset().filter(group__association = charge.levy.association)

        charge_members_queryset = AssociationMemeber.get_charge_members(
            charge, payments_associated_with_charge)

        serializer = self.get_serializer(charge_members_queryset, many=True)
        return Response(serializer.data)

