from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# Serializers
from .serializers import AssociationSerializer, AssociationGroupSerializer

# Models
from .models import Association, AssociationGroups

# Permissions
from api.permissions import IsAuthenticated, IsAssociation
class CreateAssociation(CreateAPIView):
    # POST
    serializer_class = AssociationSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    

class AssociationDetailView(RetrieveUpdateAPIView):
    # GET, PUT, PATCH
    serializer_class = AssociationSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    queryset = Association.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated,)



class CreateAssociationGroup(CreateAPIView):
    # POST
    serializer_class = AssociationGroupSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated,)
    

class AssociationGroupDetailView(RetrieveUpdateAPIView):
    # GET, PUT, PATCH
    serializer_class = AssociationGroupSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    queryset = AssociationGroups.objects.all()
    permission_classes = (IsAuthenticated, IsAssociation)

