from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AssociationLevy, AssociationLevyCharge, AssociationPayment

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


@admin.register(AssociationPayment)
class AssociationPaymentAdmin(ModelAdmin):

    list_display = ('member', 'charge', 'amount', 'date_paid')


