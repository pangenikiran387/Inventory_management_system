from django.db import models

from products.models import Products

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    from products.models import Products

class SalesOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('ESEWA', 'eSewa'),
    ]

    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    ]

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='COD')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"SO-{self.id}"


class SalesItem(models.Model):
    sales = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    selling_price = models.FloatField()

    def total(self):
        return self.quantity * self.selling_price