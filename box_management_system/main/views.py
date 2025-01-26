from django.shortcuts import render, redirect, get_object_or_404
from .models import Box, Order, OrderItem, Coupon
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

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
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        date_of_collection = request.POST.get('date_of_collection')
        address = request.POST.get('address')
        coupon_code = request.POST.get('coupon_code', '').strip()

        # Calculate total price
        total = 0
        for box_id, quantity in cart.items():
            box = Box.objects.get(id=box_id)
            total += box.price * quantity

        # Apply coupon discount if valid
        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                if coupon.is_valid():
                    discount = (coupon.discount_percentage / 100) * total
                    total -= discount
                else:
                    coupon = None
            except Coupon.DoesNotExist:
                coupon = None

        # Create order
        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            date_of_collection=date_of_collection,
            address=address,
            coupon=coupon
        )

        for box_id, quantity in cart.items():
            box = Box.objects.get(id=box_id)
            OrderItem.objects.create(
                order=order,
                box=box,
                quantity=quantity
            )
            # Update stock
            box.stock -= quantity
            box.save()

        # Send confirmation email
        subject = 'Order Confirmation'
        message = f'Thank you for your purchase, {customer_name}!\n\n'
        message += 'Order Details:\n'
        for item in order.items.all():
            message += f'{item.box.get_size_display()} Box (x{item.quantity})\n'
        message += f'\nTotal: ${total:.2f}\n'
        if coupon:
            message += f'Coupon Applied: {coupon.code} (-{coupon.discount_percentage}%)\n'
        message += f'\nDate of Collection: {date_of_collection}\n'
        message += f'\nWe will deliver your order to the following address:\n{address}\n'
        message += '\nThank you for shopping with us!'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [customer_email])

        # Clear the cart
        request.session['cart'] = {}
        return redirect('order_confirmation')
    return render(request, 'main/checkout.html')

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'main/order_confirmation.html', {'order': order})
