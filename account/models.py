from django.db import models
from association.models import Association, AssociationMemeber
# Create your models here.

"""Association levy (AL) -> category of charges and payments
    Association levy charge (ALC) -> charges created under a specific levy for members in an association
    Association payment (AP) -> association member payment record towards a levy charge


    * Relationship
    AL (1) ---to--- (many) ALC: one levy belongs to at least a charge, but a charge can't belong to more than one levy
    ALC (1) ---to--- (many) AP: one payment record can only belong to a charge


    * Notes:
        > A member's charges are the charges whose creation date is not earlier than the date the member was added
"""

MAX_CHARGABLE = 1_000_000

class AssociationLevy(models.Model):

    # Levy like Security,...

    association = models.ForeignKey(
        Association,
        related_name="levies",
        on_delete=models.CASCADE
    )

    label = models.CharField(
        verbose_name="Levy label", max_length=100, blank=False, null=False)

    date_created = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self) -> str:
        return f"{self.label} -- {self.association}"

    class Meta:
        db_table = "association_levies_tb"
        verbose_name = "Association levy"
        verbose_name_plural = "Association levies"
        unique_together=('association', 'label')


class AssociationLevyCharge(models.Model):

    # Levy like Security charge,...

    levy = models.ForeignKey(
        AssociationLevy,
        related_name="charges",
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        verbose_name="Levy charge", 
        max_length=100, 
        blank=False, 
        null=False,
        decimal_places=2,
        max_digits=MAX_CHARGABLE
    )

    date_created = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self) -> str:
        return f"{self.amount} -- {self.levy} -- {self.date_created}"

    class Meta:
        db_table = "association_charges_tb"
        verbose_name = "Association charge"
        verbose_name_plural = "Association charges"



class AssociationMemberAccount(models.Model):
    member = models.OneToOneField(
        AssociationMemeber,
        related_name="account",
        on_delete=models.CASCADE
    )

    balance = models.DecimalField(
        verbose_name="Account balance",
        blank=False,
        null=False,
        default=0.0,
        decimal_places=2,
        max_digits=MAX_CHARGABLE
    )

    last_updated = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self) -> str:
        return f"{self.member} -- {self.balance}"

    @classmethod
    def get_charge_members_account(cls, charge: AssociationLevyCharge):
        response = []

        # get all members associatied with charge
        # A member is associated to charge if the member joined date is
        #   later than the charge creation date.
        members_account_associated_with_charge = cls.objects.filter(
            member__member_group__association=charge.levy.association)

        # for each member, filter payments,
        # compute payments, and redy object reponse

        for account in members_account_associated_with_charge:

            member_data = {
                "amount_paid": 0,
                "amount_charged": charge.amount,
                "amount_left": charge.amount,
                "settled": False,
                "member_account": account
            }

            member_payments = AssociationMemberTransaction.objects.filter(
                charge=charge, member_account=account)

            for pay in member_payments:
                member_data['amount_paid'] += pay.amount

            amount_left = float(member_data.get('amount_charged')) - float(member_data.get('amount_paid'))
            
            if amount_left <= 0:
                member_data['amount_left'] = 0
                member_data['settled'] = True
                
            else:
                member_data['amount_left'] = amount_left

            response.append(member_data)

        return response



    class Meta:
        db_table = "association_member_account_tb"
        verbose_name = "Association member account"
        verbose_name_plural = "Association member accounts"


# Member payment model, covering topup and charge payment
class AssociationMemberTransaction(models.Model):

    member_account = models.ForeignKey(
        AssociationMemberAccount,
        related_name="transactions",
        on_delete=models.CASCADE
    )

    charge = models.ForeignKey(
        AssociationLevyCharge,
        related_name="payments",
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )

    amount = models.DecimalField(
        verbose_name="Amount Paid", 
        blank=False, 
        null=False,
        decimal_places=2,
        max_digits=MAX_CHARGABLE
    )

    topup = models.BooleanField(default=False) # indicates if it is credit(true) or debit(false)

    description = models.CharField(
        default="not specified",
        blank=True,
        max_length=200
    )

    def save(self, *args, **kwargs) -> None:
        
        if self.topup: # that is, if it is a credit kind of transaction
            # Update member account balance
            self.member_account.balance += self.amount
            self.member_account.save()
        
        return super().save(*args, **kwargs)

    date_paid = models.DateTimeField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=True)


    def __str__(self) -> str:
        return f"{self.amount} -- {self.charge} -- {self.member_account.member} -- {self.date_paid}"

    class Meta:
        db_table = "association_transactions_tb"
        verbose_name = "Association transaction"
        verbose_name_plural = "Association transactions"
