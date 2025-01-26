from django.contrib import admin
from .models import Box, Order, Coupon

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('size', 'price', 'stock')
    list_filter = ('size',)
    search_fields = ('size',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'ordered_at')
    search_fields = ('customer_name', 'customer_email')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'valid_from', 'valid_to', 'active')
    list_filter = ('active', 'valid_from', 'valid_to')
    search_fields = ('code',)

