from django.urls import reverse
from rest_framework import serializers

# Models
from association.models import Association
from .models import AssociationLevy

class LevySerializer(serializers.ModelSerializer):

    association_id = serializers.PrimaryKeyRelatedField(
        source="association",
        write_only=True,
        queryset=Association.objects.all()
    )

    url = serializers.SerializerMethodField()

    class Meta:
        model = AssociationLevy
        fields = (
            'id',
            'url',
            'association_id',
            'label',
            'date_created',
        )
    
    def get_url(self, obj):
        request = self.context['request']

        purl = reverse("levy-detail", kwargs={"pk": int(obj.pk)})

        return request.build_absolute_uri(purl)
