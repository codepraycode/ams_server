# from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Validators
from rest_framework.validators import UniqueValidator

# Serializers
from rest_framework import serializers

# Models
from .models import Association, AssociationGroups

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

