from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page to view products
    path('cart/', views.cart, name='cart'),  # Cart page
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add to cart
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove from cart
    path('checkout/', views.checkout, name='checkout'),  # Checkout page
    path('success/', views.success, name='success'),  # Order success page
]
