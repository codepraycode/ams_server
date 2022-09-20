from django.urls import reverse
from rest_framework import serializers

# Models
from association.models import Association
from .models import AssociationLevy, AssociationLevyCharge

class LevySerializer(serializers.ModelSerializer):

    association_id = serializers.PrimaryKeyRelatedField(
        source="association",
        write_only=True,
        queryset=Association.objects.all()
    )

    url = serializers.SerializerMethodField()
    charges_url = serializers.SerializerMethodField()

    class Meta:
        model = AssociationLevy
        fields = (
            'id',
            'label',
            'association_id',
            'url',
            'charges_url',
            'date_created',
        )
    
    def get_url(self, obj):
        request = self.context['request']

        purl = reverse("levy-detail", kwargs={"pk": obj.pk})

        return request.build_absolute_uri(purl)
    
    def get_charges_url(self, obj):
        request = self.context['request']

        purl = reverse("levycharges",
                       kwargs={
                        "levyId": obj.association.pk,
        })

        return request.build_absolute_uri(purl)

class LevyChargeSerializer(serializers.ModelSerializer):

    levy_id = serializers.PrimaryKeyRelatedField(
        source="levy",
        write_only=True,
        queryset=AssociationLevy.objects.all()
    )

    url = serializers.SerializerMethodField()
    

    class Meta:
        model = AssociationLevyCharge
        fields = (
            'id',
            'url',
            'levy_id',
            'amount',
            'date_created',
        )
    
    def get_url(self, obj):
        request = self.context['request']

        purl = reverse("levycharge-detail",
                       kwargs={
                        "pk": int(obj.pk),
                        "levyId": obj.levy.association.pk, 
                    })

        return request.build_absolute_uri(purl)
