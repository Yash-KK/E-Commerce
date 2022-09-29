from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category
)
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):    
    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 30px;"  />'.format(obj.category_image.url))
    image_tag.short_description = 'Image'
    
    list_display = ['id', 'image_tag', 'category_name', 'category_slug']
    list_display_links = ['id', 'image_tag', 'category_name']      
    list_filter = ['category_name']    
    
   
    prepopulated_fields = {'category_slug': ('category_name',), }
admin.site.register(Category, CategoryAdmin)

