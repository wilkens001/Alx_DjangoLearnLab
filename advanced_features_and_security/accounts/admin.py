from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Add the extra fields to the admin add/change forms
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')


admin.site.register(CustomUser, CustomUserAdmin)
