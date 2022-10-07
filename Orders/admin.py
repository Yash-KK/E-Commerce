from django.contrib import admin

from .models import (
    Payment,
    Order,
    OrderProduct
)
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['payment', 'user', 'product', 'order', 'variations', 'quantity', 'product_price', 'ordered']
    extra: 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'order_number', 'phone', 'order_total', 'is_ordered', 'created_at']
    search_fields = ['first_name', 'order_total']
    list_filter = ['order_total', 'is_ordered']
    
    inlines = [OrderProductInline]
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
