from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# Serializers
from .serializers import AssociationSerializer, AssociationGroupSerializer, AssociationMemberSerializer

# Models
from .models import Association, AssociationGroups, AssociationMemeber

# Permissions
from api.permissions import IsAuthenticated, IsAssociation, IsAssociationMember
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





class CreateAssociationMember(ListCreateAPIView):
    # POST
    serializer_class = AssociationMemberSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticated, IsAssociationMember)
    queryset = AssociationMemeber.objects.all()
    

class AssociationMemberDetailView(RetrieveUpdateAPIView):
    # GET, PUT, PATCH
    serializer_class = AssociationMemberSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    queryset = AssociationMemeber.objects.all()
    permission_classes = (IsAuthenticated, IsAssociationMember)

