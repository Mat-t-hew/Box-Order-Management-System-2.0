from django.shortcuts import render, redirect, get_object_or_404
from .models import Box, Order, Coupon
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

def product_list(request):
    boxes = Box.objects.all()
    return render(request, 'main/product_list.html', {'boxes': boxes})

def add_to_cart(request, box_id):
    box = get_object_or_404(Box, id=box_id)
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})
    if str(box_id) in cart:
        cart[str(box_id)] += quantity
    else:
        cart[str(box_id)] = quantity
    request.session['cart'] = cart

    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    order_items = []
    total = 0
    for box_id, quantity in cart.items():
        box = Box.objects.get(id=box_id)
        subtotal = box.price * quantity
        total += subtotal
        order_items.append({'box': box, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'main/cart.html', {'order_items': order_items, 'total': total})

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        date_of_collection = request.POST.get('date_of_collection')
        coupon_code = request.POST.get('coupon_code', '').strip()

        total = 0
        for box_id, quantity in cart.items():
            box = Box.objects.get(id=box_id)
            total += box.price * quantity

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

        for box_id, quantity in cart.items():
            box = Box.objects.get(id=box_id)
            order = Order.objects.create(
                box=box,
                quantity=quantity,
                customer_name=customer_name,
                customer_email=customer_email,
                date_of_collection=date_of_collection,
                coupon=coupon
            )
            box.stock -= quantity
            box.save()

        subject = 'Order Confirmation'
        message = f'Thank you for your purchase, {customer_name}!\n\n'
        message += 'Order Details:\n'
        for box_id, quantity in cart.items():
            box = Box.objects.get(id=box_id)
            message += f'{box.get_size_display()} Box (x{quantity})\n'
        message += f'\nTotal: ${total:.2f}\n'
        if coupon:
            message += f'Coupon Applied: {coupon.code} (-{coupon.discount_percentage}%)\n'
        message += f'\nDate of Collection: {date_of_collection}\n'
        message += '\nThank you for shopping with us!'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [customer_email])

        request.session['cart'] = {}
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'main/checkout.html')

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'main/order_confirmation.html', {'order': order})
