from django.db import models

# Inventory Model (Product Catalog)
class Inventory(models.Model):
    name = models.CharField(max_length=100)
    dimensions = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.dimensions})"

# Cart Model
class Cart(models.Model):
    session_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

# Cart Item Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity

# Order Model
class Order(models.Model):
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    items = models.ManyToManyField(Inventory, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.client_name}"

# Order Item Model (Links Orders and Inventory with Quantity)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity
