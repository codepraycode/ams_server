from rest_framework.generics import GenericAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

# # Mixins
# from rest_framework.mixins import CreateModelMixin

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

    def retrieve(self, request, *args, **kwargs):
        instance = request.association # self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = request.association  # self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    

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

