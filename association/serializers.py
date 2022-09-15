# from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from association.models import Association


class AssociationSerializer(serializers.Serializer):
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

    email = serializers.EmailField(
        label=_("Email"),
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )


    def create(self, validated_data):
        instance = Association.objects.create_association(**validated_data)

        return instance
