from django.db import models
from django.utils import timezone

class Box(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.get_size_display()} Box"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to

class Order(models.Model):
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    date_of_collection = models.DateField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"

    def get_total_cost(self):
        total = self.box.price * self.quantity
        if self.coupon and self.coupon.is_valid():
            discount = (self.coupon.discount_percentage / 100) * total
            total -= discount
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.id} for Order {self.order.id}"
