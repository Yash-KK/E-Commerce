from django.contrib import admin
from .models import (
    Cart,
    CartItems
)
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id']
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product','quantity']    
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItems, CartItemAdmin)
