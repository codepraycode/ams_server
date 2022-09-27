from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Association, AssociationGroups, AssociationMemeber

from django.contrib.admin import ModelAdmin
# Register your models here.
# admin.site.register(SchoolOwner, UserAdmin)


@admin.register(Association)
class AssociationAdmin(ModelAdmin):

    list_display = ('name', 'email','registration_id', 'local_government', 'is_verified',
                    'is_active',)
    search_fields = ('name', 'email', 'registration_id')


@admin.register(AssociationGroups)
class AssociationGroupsAdmin(ModelAdmin):

    list_display = ('association', 'name', 'date_created',)
    search_fields = ('name',)


@admin.register(AssociationMemeber)
class AssociationMemberAdmin(ModelAdmin):

    list_display = ('association', 'name', 'date_joined',)
    search_fields = ('first_name', 'last_name')

    def association(self, obj):
        return f"{obj.group.association}"
    
    def name(self, obj):
        return obj.full_name

