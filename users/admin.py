# users/admin.py - CORRECTED VERSION
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser
    """
    model = CustomUser
    list_display = ['username', 'email', 'date_joined', 'is_active_member', 'is_staff']
    
    
    fieldsets = UserAdmin.fieldsets + (
        
        ('Library Information', {
            'fields': ('date_of_membership', 'is_active_member', 'phone_number'),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Library Information', {
            'fields': ('date_of_membership', 'is_active_member', 'phone_number'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)