from enum import unique
from django.db import models

from .models_utils import (
    AssociationModelBase, AssociationManager, handle_upload_logo, handle_upload_passport)

# from django.utils.crypto import get_random_string, salted_hmac
# from django.conf import settings

from django.utils.translation import gettext_lazy as _


class Association(AssociationModelBase):
    logo = models.ImageField(
        _("Logo"), upload_to=handle_upload_logo, null=True, blank=True)

    name = models.CharField(
        verbose_name="Association name", max_length=255, blank=False, null=False)
    registration_id = models.CharField(
        verbose_name="Association registration", max_length=255, blank=False, null=False)

    contact = models.CharField(
        verbose_name="Contact", max_length=100, null=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    town = models.CharField(
        verbose_name="Town", max_length=100, null=False)
    city = models.CharField(
        verbose_name="City", max_length=100, null=False)
    local_government = models.CharField(
        verbose_name="Local government", max_length=100, null=False)
    country = models.CharField(
        verbose_name="Country", max_length=100, null=False)

    group_label = models.CharField(
        verbose_name="Group Label", max_length=100, default="streets", null=False)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, editable=True)

    # USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = AssociationManager()


    class Meta:
        db_table = "associations_tb"
        verbose_name = "Association"
        verbose_name_plural = "Associations"


class AssociationGroups(models.Model):

    # a group/street has to belong to one association
    association = models.ForeignKey(
        Association,
        related_name="groups",
        # related_query_name="association",
        on_delete=models.CASCADE
    )

    name = models.CharField(
        verbose_name="Association name", max_length=255, blank=False, null=False)

    date_created = models.DateTimeField(auto_now_add=True, editable=True)


    def __str__(self) -> str:
        return f"{self.name} -- {self.association}"
    class Meta:
        db_table = "association_groups_tb"
        verbose_name = "Association group"
        verbose_name_plural = "Association groups"


class AssociationMemeber(models.Model):
    passport = models.ImageField(
        _("Passport"), upload_to=handle_upload_passport, null=True, blank=True)

    first_name = models.CharField(
        verbose_name="Member first name", max_length=255, blank=False, null=False)
    last_name = models.CharField(
        verbose_name="Member last name", max_length=255, blank=False, null=False)
    
    group_id = models.CharField(
        verbose_name="Member group identification", max_length=100, blank=False, null=False)


    member_group = models.ForeignKey(
        AssociationGroups,
        related_name="members",
        on_delete=models.CASCADE
    )

    contact = models.CharField(
        verbose_name="Member contact", max_length=100, null=False)
    
    gender = models.CharField(
        verbose_name="Member gender", max_length=10, null=False)
    
    date_of_birth = models.DateField(verbose_name="Member date of birth", null=False)

    religion = models.CharField(
        verbose_name="Member religion", max_length=100, null=False)
    
    nationality = models.CharField(
        verbose_name="Member nationality", max_length=100, null=False)
    
    state_of_origin = models.CharField(
        verbose_name="Member state of origin", max_length=100, null=False)
    
    ethnicity = models.CharField(
        verbose_name="Member ethnicity", max_length=100, null=False)
    
    local_government_of_origin = models.CharField(
        verbose_name="Member local government of origin", max_length=100, null=False)
    
    occupation = models.CharField(
        verbose_name="Member occupation", max_length=100, null=False)
    
    next_of_kin = models.CharField(
        verbose_name="Member next of kin", max_length=100, null=False)
    next_of_kin_contact = models.CharField(
        verbose_name="Member next of kin contact", max_length=100, null=False)
    
    date_joined = models.DateTimeField(auto_now_add=True, editable=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self) -> str:
        return f"{self.full_name} -- {self.member_group.association}"
    
    @classmethod
    def get_charge_members(cls, charge, payments_associated_with_charge):
        response = []

        # get all members associatied with charge
        # A member is associated to charge if the member joined date is
        #   later than the charge creation date.
        members_associated_with_charge = cls.objects.filter(
            group__association=charge.levy.association)

        # for each member, filter payments,
        # compute payments, and redy object reponse

        for member in members_associated_with_charge:
            member_data = {
                "amount_paid": 0,
                "amount_charged": charge.amount,
                "amount_left": charge.amount,
                "settled": False,
                "member":member
            }

            member_payments = payments_associated_with_charge.filter(
                member=member)

            for pay in member_payments:
                member_data['amount_paid'] += pay.amount

            amount_left = float(member_data.get('amount_charged')) - float(member_data.get('amount_paid'))
            
            # if amount_left >= float(member_data.get('amount_charged')):
            #     member_data['amount_left'] = amount_left
            if amount_left <= 0:
                member_data['amount_left'] = 0
                member_data['settled'] = True
            else:
                member_data['amount_left'] = amount_left

            response.append(member_data)

        return response


    class Meta:
        db_table = "association_memeber_tb"
        verbose_name = "Association Member"
        verbose_name_plural = "Association Members"
