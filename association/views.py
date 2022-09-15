from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# Serializers
from .serializers import AssociationSerializer

# Models
from .models import Association

# Permissions
from api.permissions import IsAuthenticated
class CreateAssociation(CreateAPIView):
    # POST
    serializer_class = AssociationSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    


class AssociationView(RetrieveUpdateAPIView):
    # GET, PUT, PATCH
    serializer_class = AssociationSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    queryset = Association.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated,)
    
