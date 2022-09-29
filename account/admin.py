from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    AssociationLevy, 
    AssociationLevyCharge, 
    AssociationMemberAccount,
    AssociationMemberTransaction
)

from django.contrib.admin import ModelAdmin

# Register your models here.

@admin.register(AssociationLevy)
class AssociationLevyAdmin(ModelAdmin):

    list_display = ('label', 'association', 'date_created',)
    search_fields = ('label', )

    # def association(self, obj):
    #     return f"{obj.association}"


@admin.register(AssociationLevyCharge)
class AssociationLevyChargeAdmin(ModelAdmin):

    list_display = ('levy', 'amount', 'date_created',)
    # search_fields = ('name',)


@admin.register(AssociationMemberAccount)
class AssociationMemberAccountAdmin(ModelAdmin):

    list_display = ('member', 'balance', 'last_updated',)

@admin.register(AssociationMemberTransaction)
class AssociationMemberTransactionAdmin(ModelAdmin):

    list_display = ('member', 'charge', 'amount', 'description', 'topup', 'date_paid')

    def member(self, obj):
        return obj.member_account.member


