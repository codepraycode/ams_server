from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Validators
from rest_framework.validators import UniqueValidator

# Serializers
from rest_framework import serializers
from account.serializers import LevySerializer, AssociationMemberAccountSerializer

# Models
from .models import Association, AssociationGroups, AssociationMemeber
from account.models import AssociationMemberAccount
# Exceptions
from rest_framework.exceptions import ValidationError

class AssociationGroupSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()

    name = serializers.CharField(
        label=_("Name"),
    )
    date_created = serializers.DateTimeField(
        label=_("Date Created"),
        read_only=True,
    )

    class Meta:
        model = AssociationGroups
        fields = (
            'id',
            'name',
            'url',
            'date_created'
        )
    

    def get_url(self, obj):
        request = self.context['request']

        purl = reverse("associationgroup-detail", kwargs={"pk":int(obj.pk)})

        return request.build_absolute_uri(purl)
    
    def create(self, validated_data):

        request = self.context['request']

        name = validated_data.get('name', '')
        # association = validated_data.get('association', '')
        association = request.association

        any_name = AssociationGroups.objects.filter(
            association=association, name=name).exists()

        if any_name:
            raise ValidationError({"error":"Name already taken"}, code='unique')
        
        validated_data['association'] = association
        return super().create(validated_data)


class AssociationSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(
        label=_("Logo"),
        required=True,
        # write_only=True
    )
    name = serializers.CharField(
        label=_("Name"),
    )
    registration_id = serializers.CharField(
        label=_("Registration Id"),
    )
    contact = serializers.CharField(
        label=_("Contact"),
    )
    
    town = serializers.CharField(
        label=_("Town"),
    )
    city = serializers.CharField(
        label=_("City"),
    )
    local_government = serializers.CharField(
        label=_("Local government"),
    )
    country = serializers.CharField(
        label=_("Country"),
    )

    group_label = serializers.CharField(
        label=_("Groups label"),
    )

    groups = AssociationGroupSerializer(many=True, read_only=True)
    levies = LevySerializer(many=True, read_only=True)

    email = serializers.EmailField(
        label=_("Email"),
        validators=[UniqueValidator(queryset=Association.objects.all())]
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    
    class Meta:
        model = Association
        fields = (
            'id',
            'logo',
            'name',
            'registration_id',
            'contact',
            'town',
            'city',
            'local_government',
            'country',

            'email',
            'password',
            
            "group_label",
            'groups',
            'levies',
        )

    def create(self, validated_data):
        # return super().create(validated_data)
        return Association.objects.create_association(**validated_data)

class AssociationMemberSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    passport = serializers.ImageField(
        label=_("Passport"),
        required=False,
        write_only=True
    )
    passport_url = serializers.SerializerMethodField()

    group = serializers.PrimaryKeyRelatedField(
        source="member_group",
        write_only=True,
        queryset=AssociationGroups.objects.all()
    )

    group_url = serializers.SerializerMethodField()

    account = AssociationMemberAccountSerializer(read_only=True)

    # def get_account(self, obj):
    #     print(obj.account)
    #     return {}

    def get_url(self, obj):
        request = self.context['request']

        purl = reverse("associationmember-detail", kwargs={"pk": int(obj.pk)})

        return request.build_absolute_uri(purl)

    def get_group_url(self, obj):
        request = self.context['request']

        purl = reverse("associationgroup-detail",
                       kwargs={"pk": int(obj.member_group.pk)})

        return request.build_absolute_uri(purl)

    
    def get_passport_url(self, obj):
        request = self.context['request']

        purl = obj.passport.url

        return request.build_absolute_uri(purl)
    
    class Meta:
        model = AssociationMemeber
        fields = (
            'id',
            'url',
            'passport',
            'passport_url',
            'first_name',
            'last_name',
            'gender',
            'occupation',

            'group',
            'group_id',
            'group_url',
            'account',

            'contact',
            
            "date_of_birth",
            'religion',
            
            'nationality',
            'state_of_origin',
            'ethnicity',
            'local_government_of_origin',
            
            'next_of_kin',
            'date_joined',
        )

    # TODO: create member account on member creation and implement it serializer
    def create(self, validated_data):
        instance = super().create(validated_data)
        
        account = AssociationMemberAccount(member=instance)
        account.save()

        return instance

