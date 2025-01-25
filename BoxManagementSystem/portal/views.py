from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory, Cart, CartItem, Order
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
import matplotlib.pyplot as plt
import io
import urllib, base64

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

    messages.success(request, f"Added {product.name} to your cart.")
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
    messages.success(request, "Item removed from your cart.")
    return redirect('cart')

# Checkout Page - Finalize Order
def checkout(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in items)

    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

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

        messages.success(request, "Your order was placed successfully!")
        return redirect('success')

    return render(request, 'portal/checkout.html', {'items': items, 'total_price': total_price})

# Success Page
def success(request):
    return render(request, 'portal/success.html')

# Admin Dashboard with Sales Chart
@staff_member_required
def admin_dashboard(request):
    sales_data = Order.objects.values('created_at__date').annotate(total_sales=Sum('total_price')).order_by('created_at__date')

    # Generate Sales Chart
    dates = [data['created_at__date'] for data in sales_data]
    sales = [data['total_sales'] for data in sales_data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, sales, marker='o', linestyle='-', color='b')
    plt.title('Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sales (R)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'portal/admin_dashboard.html', {'chart': uri})
