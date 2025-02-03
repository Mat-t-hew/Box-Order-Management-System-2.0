from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models import Sum

# Create your models here.

class Box_Type(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default='1')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Box(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField()
    price = models.FloatField(default=0)
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default='1')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def count_inventory(self):
        stocks = Stock.objects.filter(box=self)
        stock_in = stocks.filter(type='1').aggregate(Sum('quantity'))['quantity__sum'] or 0
        stock_out = stocks.filter(type='2').aggregate(Sum('quantity'))['quantity__sum'] or 0
        return stock_in - stock_out

class Stock(models.Model):
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    type = models.CharField(max_length=2, choices=(('1', 'Stock-in'), ('2', 'Stock-Out')), default='1')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.box.code} - {self.box.name}"

class Invoice(models.Model):
    transaction = models.CharField(max_length=250)
    customer = models.CharField(max_length=250)
    total = models.FloatField(default=0)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction

    def item_count(self):
        return InvoiceItem.objects.filter(invoice=self).aggregate(Sum('quantity'))['quantity__sum']

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return self.invoice.transaction

@receiver(models.signals.post_save, sender=InvoiceItem)
def stock_update(sender, instance, **kwargs):
    stock = Stock(box=instance.box, quantity=instance.quantity, type='2')
    stock.save()
    InvoiceItem.objects.filter(id=instance.id).update(stock=stock)

@receiver(models.signals.post_delete, sender=InvoiceItem)
def delete_stock(sender, instance, **kwargs):
    if instance.stock:
        try:
            instance.stock.delete()
        except Stock.DoesNotExist:
            pass
