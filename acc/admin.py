from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Models
from .models import (
    Account,
    UserProfile
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

class UserProfileAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 30px;"  />'.format(obj.profile_pic.url))
    image_tag.short_description = 'Image'
    list_display = ['user', 'image_tag', 'city', 'country']
   
    
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
