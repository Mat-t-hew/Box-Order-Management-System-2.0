from django.contrib import admin
from .models import Box, Order, OrderItem, Coupon

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('size', 'price', 'stock')
    list_filter = ('size',)
    search_fields = ('size',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'order_status', 'created_at', 'ordered_at')
    search_fields = ('customer_name', 'customer_email')
    inlines = [OrderItemInline]

    def order_status(self, obj):
        # Define how to determine the order status
        return "Status"

    def created_at(self, obj):
        return obj.ordered_at.date()

    order_status.short_description = 'Order Status'
    created_at.short_description = 'Created At'

admin.site.register(Coupon)
