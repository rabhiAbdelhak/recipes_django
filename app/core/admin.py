# user admin customization.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models


class UserAdmin(BaseUserAdmin):
    # define the admin pages for users.
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        ('Personal information', {'fields': ('email', 'password')}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        ('Important Dates', {'fields': ('last_login',)})

    )
    readonly_fields = ['last_login']

    add_fieldsets = (
        'User Information',
        {'classes': ('wide',),
         'fields': (
            'name',
            'email',
            'password1',
            'password2',
            'is_superuser',
            'is_active',
            'is_staff',
        )
        },
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
