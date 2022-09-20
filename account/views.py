from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

# Parsers
from rest_framework.parsers import (MultiPartParser, FormParser, JSONParser)

# Permissions
from api.permissions import IsAuthenticated, IsAssociationLevy

# Serializers
from .serializers import LevySerializer

# Models
from .models import AssociationLevy

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
