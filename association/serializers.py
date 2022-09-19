from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Validators
from rest_framework.validators import UniqueValidator

# Serializers
from rest_framework import serializers

# Models
from .models import Association, AssociationGroups, AssociationMemeber

# Exceptions
from rest_framework.exceptions import ValidationError

class AssociationGroupSerializer(serializers.ModelSerializer):
    association_id = serializers.PrimaryKeyRelatedField(
        source="association",
        write_only=True,
        queryset=Association.objects.all()
    )

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
            'association_id',
            'name',
            'url',
            'date_created'
        )
    

    def get_url(self, obj):
        request = self.context['request']

        purl = reverse("associationgroup-detail", kwargs={"pk":int(obj.pk)})

        return request.build_absolute_uri(purl)
    
    def create(self, validated_data):

        
        name = validated_data.get('name', '')
        association = validated_data.get('association', '')

        any_name = AssociationGroups.objects.filter(
            association=association, name=name).exists()

        if any_name:
            raise ValidationError({"error":"Name already taken"}, code='unique')

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
            'contact',
            'town',
            'city',
            'local_government',
            'country',
            "group_label",
            'groups',
            'email',
            'password',
        )


    # def create(self, validated_data):
    #     instance = Association.objects.create_association(**validated_data)

    #     return instance

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class AssociationMemberSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    passport = serializers.ImageField(
        label=_("Passport"),
        required=False,
        write_only=True
    )
    passport_url = serializers.SerializerMethodField()

    group_id = serializers.PrimaryKeyRelatedField(
        source="group",
        write_only=True,
        queryset=AssociationGroups.objects.all()
    )

    group_url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context['request']

        purl = reverse("associationmember-detail", kwargs={"pk": int(obj.pk)})

        return request.build_absolute_uri(purl)

    def get_group_url(self, obj):
        request = self.context['request']

        purl = reverse("associationgroup-detail", kwargs={"pk": int(obj.group.pk)})

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

            'group_no',
            'group_id',
            'group_url',

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


