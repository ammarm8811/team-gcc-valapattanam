from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'email',
        'full_name',
        'phone_whatsapp',
        'blood_group',
        'role',
        'is_active',
    )

    ordering = ('email',)

    search_fields = (
        'email',
        'full_name',
        'phone_whatsapp',
    )

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            )
        }),

        ('Personal Information', {
            'fields': (
                'full_name',
                'phone_whatsapp',
                'dob',
                'blood_group',
            )
        }),

        ('Role & Permissions', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'full_name',
                'phone_whatsapp',
                'password1',
                'password2',
                'role',
                'is_staff',
                'is_active',
            )
        }),
    )