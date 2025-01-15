from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory, Cart, CartItem, Order
from django.http import JsonResponse

# Helper: Get or create a cart
def get_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

# Home Page - Show Products
def home(request):
    products = Inventory.objects.all()
    return render(request, 'portal/home.html', {'products': products})

# Add Product to Cart
def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Inventory, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

# Cart Page - Display Cart Items
def cart(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in items)
    return render(request, 'portal/cart.html', {'items': items, 'total_price': total_price})

# Remove Item from Cart
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')

# Checkout Page - Finalize Order
def checkout(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in items)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']

        # Create Order
        order = Order.objects.create(client_name=name, client_email=email, total_price=total_price)

        # Link Cart Items to the Order
        for item in items:
            order.items.add(item.product)
        
        # Clear Cart
        items.delete()

        return redirect('success')

    return render(request, 'portal/checkout.html', {'items': items, 'total_price': total_price})

# Success Page
def success(request):
    return render(request, 'portal/success.html')
