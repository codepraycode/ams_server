from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Association

from django.contrib.admin import ModelAdmin
# Register your models here.
# admin.site.register(SchoolOwner, UserAdmin)


@admin.register(Association)
class AssociationAdmin(ModelAdmin):

    list_display = ('name', 'email', 'local_government', 'is_verified',
                    'is_active',)
    search_fields = ('name', 'email', )
    # fieldsets = (
    #     (None, {'fields': ('name', 'password')}),
    #     (_('Personal info'), {
    #      'fields': ('avatar', 'firstname', 'lastname', 'email')}),
    #     (_('Permissions'), {
    #         'fields': ('is_active', 'is_staff', 'is_verified', 'is_superuser', 'groups', 'user_permissions'),
    #     }),
    #     (_('Important dates'), {'fields': ('last_login',)}),
    # )
