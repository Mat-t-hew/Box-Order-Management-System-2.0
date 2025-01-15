from django.contrib import admin
from .models import Inventory, Order, Cart, CartItem, OrderItem

admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
