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

# Exceptions
from rest_framework.exceptions import PermissionDenied, NotAcceptable


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
                        # "levyId": obj.levy.association.pk, 
                    })

        return request.build_absolute_uri(purl)
    
    def get_payment_url(self, obj):
        request = self.context['request']

        purl = reverse("levycharge-payment")

        return request.build_absolute_uri(purl)
    
    def get_members_url(self, obj):
        request = self.context['request']

        purl = reverse("levychargemembers-detail",
                       kwargs={
                        "chargePk": obj.pk,
                        }
        )

        return request.build_absolute_uri(purl)


    def create(self, validated_data):
        request = self.context['request']
        if validated_data['levy'].association.pk != request.association.pk:
            raise PermissionDenied("You are not allowed to create this levy")
        return super().create(validated_data)


class LevySerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()
    create_charges_url = serializers.SerializerMethodField()

    charges = LevyChargeSerializer(read_only=True, many=True)

    class Meta:
        model = AssociationLevy
        fields = (
            'id',
            'label',
            'url',
            'date_created',
            'create_charges_url',
            'charges',
        )

    def get_url(self, obj):
        request = self.context['request']

        purl = reverse("levy-detail", kwargs={"pk": obj.pk})

        return request.build_absolute_uri(purl)

    def get_create_charges_url(self, obj):
        request = self.context['request']

        purl = reverse("levycharges")

        return request.build_absolute_uri(purl)

    def create(self, validated_data):
        request = self.context['request']
        validated_data['association'] = request.association

        return super().create(validated_data)


class AssociationChargeMemberSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    member_id = serializers.IntegerField()

    balance = serializers.DecimalField(
        max_digits=MAX_CHARGABLE,
        min_value=0.00,
        decimal_places=2
    )

    def get_member_id(self, obj):
        
        return obj.member.pk


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
    

class CreateAssociationMemberPaymentSerializer(serializers.ModelSerializer):

    # Posting payment
    # like a receipt for a successful payment

    charge_id = serializers.PrimaryKeyRelatedField(
        source="charge",
        queryset=AssociationLevyCharge.objects.all(),
        default=None,
    )
    account_id = serializers.PrimaryKeyRelatedField(
        source="member_account",
        queryset=AssociationMemberAccount.objects.all(),
        required=True
    )
    amount_paid = serializers.DecimalField(
        source="amount",
        max_digits=MAX_CHARGABLE,
        min_value=0.00,
        decimal_places=2,
        required=True
    )
    topup = serializers.BooleanField(default=False)
    from_account = serializers.BooleanField(default=False)


    class Meta:
        model = AssociationMemberTransaction
        fields = (
            'charge_id',
            'account_id',
            'amount_paid',
            'topup',
            'from_account',
            'date_paid',
            'date_created',
        )
    
    def create(self, validated_data):
        # Validate payload
        # if charge is none, then set topup to true
        #  like auto top up if charge not found

        # also check that the account belongs to association
        # also check that amount is greater than 0.0

        request = self.context['request']

        account = validated_data.get('member_account', None)

        if not account or account.member.member_group.association.pk != request.association.pk:
            raise PermissionDenied("You have no permission to operate on this member account") # 403
        
        charge = validated_data.get('charge', None)

        if charge and charge.levy.association.pk != request.association.pk:
            raise PermissionDenied(
                "You have no permission to operate on this levy charge")  # 403

        # All is set
        amount = float(validated_data.get('amount', 0.0))
        from_account = validated_data.pop('from_account', False)

        # Auto topup member account
        isTopUp = validated_data.get('topup', False)
        
        if isTopUp:
            pass
        elif not charge:
            validated_data['topup'] = True
        else: # if it is a charge

            if amount <= 100.0: # least amount allowed
                raise NotAcceptable("Amount too small")


            # Fetch all member charge payment transactions
            member_payments = AssociationMemberTransaction.objects.filter(
                charge=charge, member_account=account)
            

            debt = float(charge.amount) # debt is charge amount

            # Go through each payment and reduce debt by amount paid
            for each_pay in member_payments:
                payment = float(each_pay.amount)

                if debt <= 0.0: # break if debt is already settled
                    debt = 0.0
                    break

                debt = debt - payment if debt > payment else 0
            
            if debt <= 0.0:
                raise NotAcceptable(
                    "Charge already settled")  # 406

            # the technique will use account balance if from account is set
            #  else it will combine the account balance with amount sent
            # then the debt will be settled from the combination

            balance = account.balance if from_account else amount + float(account.balance)

            balance_left = float(balance) - debt


            # amount paid is the amount sent if the debt is not less than the amount
            # otherwise the debt
            amount_paid = amount if debt >= amount else debt

            # new acocunt balance will be 0 if balance left is 0
            # otherwise the balance left
            account.balance = balance_left if balance_left > 0 else 0
            account.save() # save member account update
            
            # update amount paid
            # this will prevent overflow in charge payment
            validated_data['amount'] = amount_paid 
            
            
        return super().create(validated_data)


class AssociationMemberPaymentSerializer(serializers.Serializer):

    # This one is used when querying all the members under a levy charge
    # the computation is done in the model, and the data(result) is
    # serialized here

    member_account = AssociationChargeMemberSerializer(read_only=True)
    
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
