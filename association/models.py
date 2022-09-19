from django.db import models

from .models_utils import (
    AssociationModelBase, AssociationManager, handle_upload_dir)

# from django.utils.crypto import get_random_string, salted_hmac
# from django.conf import settings

from django.utils.translation import gettext_lazy as _


class Association(AssociationModelBase):
    logo = models.ImageField(
        _("Logo"), upload_to=handle_upload_dir, null=True, blank=True)

    name = models.CharField(
        verbose_name="Associatin name", max_length=255, blank=False, null=False)

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
        verbose_name="Associatin name", max_length=255, blank=False, null=False)

    date_created = models.DateTimeField(auto_now_add=True, editable=True)

    class Meta:
        db_table = "association_groups_tb"
        verbose_name = "Association group"
        verbose_name_plural = "Association groups"
