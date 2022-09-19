from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Association, AssociationGroups

from django.contrib.admin import ModelAdmin
# Register your models here.
# admin.site.register(SchoolOwner, UserAdmin)


@admin.register(Association)
class AssociationAdmin(ModelAdmin):

    list_display = ('name', 'email', 'local_government', 'is_verified',
                    'is_active',)
    search_fields = ('name', 'email', )


@admin.register(AssociationGroups)
class AssociationGroupsAdmin(ModelAdmin):

    list_display = ('association', 'name', 'date_created',)
    search_fields = ('name',)

