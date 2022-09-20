from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView\

# Parsers
from rest_framework.parsers import (MultiPartParser, FormParser, JSONParser)

# Permissions
from api.permissions import IsAuthenticated, IsAssociationLevy, IsAssociationLevyCharge

# Serializers
from .serializers import LevySerializer, LevyChargeSerializer

# Models
from .models import AssociationLevy, AssociationLevyCharge

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
