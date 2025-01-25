from django.contrib import admin
from .models import Box, Order, OrderItem

# Register your models here.

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
    list_display = ('id', 'customer_name', 'customer_email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_email')
    inlines = [OrderItemInline]
