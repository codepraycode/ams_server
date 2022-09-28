from django.urls import reverse
from rest_framework import serializers

# Models
from association.models import Association, AssociationMemeber
from .models import (
    AssociationLevy, 
    AssociationLevyCharge, 
    MAX_CHARGABLE, 
    AssociationMemberTransaction, 
    AssociationMemberAccount
)

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
    payment_url = serializers.SerializerMethodField()
    members_url = serializers.SerializerMethodField()
    
    

    class Meta:
        model = AssociationLevyCharge
        fields = (
            'id',
            'url',
            'levy_id',
            'amount',
            'payment_url',
            'members_url',
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
    
    def get_payment_url(self, obj):
        request = self.context['request']

        purl = reverse("levycharge-payment",
                       kwargs={
                        "levyId": obj.levy.association.pk,
                        "chargeId":obj.pk,
        })

        return request.build_absolute_uri(purl)
    
    def get_members_url(self, obj):
        request = self.context['request']

        purl = reverse("levychargemembers-detail",
                       kwargs={
                        "levyId": obj.levy.association.pk,
                        "chargeId":obj.pk,
        })

        return request.build_absolute_uri(purl)


class AssociationChargeMemberSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    url = serializers.SerializerMethodField()
    passport_url = serializers.SerializerMethodField()

    group_url = serializers.SerializerMethodField()

    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)
    occupation = serializers.CharField(read_only=True)
    contact = serializers.CharField(read_only=True)
    

    def get_url(self, obj):
        request = self.context['request']

        purl = reverse("associationmember-detail", kwargs={"pk": int(obj.pk)})

        return request.build_absolute_uri(purl)

    def get_group_url(self, obj):
        request = self.context['request']

        purl = reverse("associationgroup-detail",
                       kwargs={"pk": int(obj.group.pk)})

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


class AssociationMemberAccountSerializer(serializers.Serializer):
    account_id = serializers.IntegerField(source="id", read_only=True)
    topup_url = serializers.SerializerMethodField()

    balance = serializers.DecimalField(
        max_digits=MAX_CHARGABLE,
        min_value=0.00,
        decimal_places=2
    )

    last_updated = serializers.DateTimeField(read_only=True)


    def get_topup_url(self, obj):
        request = self.context['request']

        purl = reverse("member-topup")

        return request.build_absolute_uri(purl)
    

class CreateAssociationPaymentSerializer(serializers.ModelSerializer):

    # Posting payment
    # like a receipt for a successful payment

    charge_id = serializers.PrimaryKeyRelatedField(
        source="charge",
        queryset=AssociationLevyCharge.objects.all(),
        default=None,
    )
    account_id = serializers.PrimaryKeyRelatedField(
        source="member_account",
        queryset=AssociationMemberAccount.objects.all()
    )
    amount_paid = serializers.DecimalField(
        source="amount",
        max_digits=MAX_CHARGABLE,
        min_value=0.00,
        decimal_places=2
    )
    topup = serializers.BooleanField(default=False)


    class Meta:
        model = AssociationMemberTransaction
        fields = (
            'charge_id',
            'account_id',
            'amount_paid',
            'topup',
            'date_paid',
            'date_created',
        )


class AssociationMemberPaymentSerializer(serializers.Serializer):

    # This one is used when querying all the members under a levy charge
    # the computation is done in the model, and the data(result) is
    # serialized here

    member = AssociationChargeMemberSerializer()
    
    # payment_url = serializers.SerializerMethodField()
    settled = serializers.BooleanField()
    
    amount_charged = serializers.DecimalField(
        max_digits=MAX_CHARGABLE,
        min_value=0.00,
        decimal_places=2
    )

    amount_paid = serializers.DecimalField(
        max_digits=MAX_CHARGABLE,
        min_value=0.00,
        decimal_places=2
    )

    amount_left = serializers.DecimalField(
        max_digits=MAX_CHARGABLE,
        min_value=0.00,
        decimal_places=2
    )
