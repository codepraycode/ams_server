from rest_framework.generics import GenericAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

# # Mixins
# from rest_framework.mixins import CreateModelMixin

# Serializers
from .serializers import AssociationSerializer, AssociationGroupSerializer, AssociationMemberSerializer

# Models
from .models import Association, AssociationGroups, AssociationMemeber

# Permissions
from api.permissions import IsAuthenticated, IsAssociationGroup, IsAssociationMember


class CreateAssociation(CreateAPIView):
    # POST, GET(to verify registration id)
    serializer_class = AssociationSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # verify if reg_id hasn't been used
        reg_id = request.GET.get('reg_id', None)

        if not reg_id:
            return Response({"message":"No reg id to validate"}, status=status.HTTP_400_BAD_REQUEST)
        
        exists = Association.objects.filter(registration_id=reg_id).exists()

        if exists:
            return Response({"message": "Associtation with registration id already exist in system"}, status=status.HTTP_409_CONFLICT)
        
        return Response({"message":"Validated!"}, status=status.HTTP_200_OK)

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
    permission_classes = (IsAuthenticated, IsAssociationGroup)


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

