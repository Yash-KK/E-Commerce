from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Models
from .models import (
    Account
)
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'is_active')
    list_filter = ('email', 'is_active',)
    # readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        # (None, {'fields': ('email', 'password')}),
        # ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        # (None, {
        #     'classes': ('wide',),
        #     'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        # ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    
    
admin.site.register(Account, AccountAdmin)
