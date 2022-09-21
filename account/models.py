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


class AssociationPayment(models.Model):

    member = models.ForeignKey(
        AssociationMemeber,
        related_name="transactions",
        on_delete=models.CASCADE
    )

    charge = models.ForeignKey(
        AssociationLevyCharge,
        related_name="payments",
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        verbose_name="Amount Paid", 
        blank=False, 
        null=False,
        decimal_places=2,
        max_digits=MAX_CHARGABLE
    )

    date_paid = models.DateTimeField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=True)


    def __str__(self) -> str:
        return f"{self.amount} -- {self.charge} -- {self.member} -- {self.date_paid}"

    class Meta:
        db_table = "association_payments_tb"
        verbose_name = "Association payment"
        verbose_name_plural = "Association payments"
