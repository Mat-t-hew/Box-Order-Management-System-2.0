from django.shortcuts import render, redirect, get_object_or_404
from .models import Box, Order, OrderItem

# Create your views here.

def product_list(request):
    boxes = Box.objects.all()
    return render(request, 'main/product_list.html', {'boxes': boxes})

def add_to_cart(request, box_id):
    box = get_object_or_404(Box, id=box_id)
    quantity = int(request.POST.get('quantity', 1))

    # Retrieve or create an active order for the session
    order, created = Order.objects.get_or_create(
        customer_name=request.session.session_key,
        status='Pending'
    )

    # Check if the box is already in the order
    order_item, item_created = OrderItem.objects.get_or_create(
        order=order,
        box=box,
    )

    if item_created:
        order_item.quantity = quantity
    else:
        order_item.quantity += quantity

    order_item.save()
    return redirect('view_cart')

def view_cart(request):
    order = Order.objects.filter(
        customer_name=request.session.session_key,
        status='Pending'
    ).first()
    return render(request, 'main/cart.html', {'order': order})

def checkout(request):
    order = Order.objects.filter(
        customer_name=request.session.session_key,
        status='Pending'
    ).first()

    if request.method == 'POST':
        # Retrieve shipping information from the form
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')

        # Save shipping information to the order
        order.full_name = full_name
        order.address = address
        order.city = city
        order.postal_code = postal_code
        order.country = country
        order.status = 'Completed'
        order.save()

        # Redirect to an order confirmation page
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'main/checkout.html', {'order': order})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'main/order_confirmation.html', {'order': order})
