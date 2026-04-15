from django.utils import timezone
from email.policy import default
import random

from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name
class Supplier(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(blank=True)
    phone=models.CharField(max_length=20)
    address=models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.IntegerField(default=0)
    low_stock_threshold = models.PositiveBigIntegerField(default=5)
    stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            category_code = self.category.name[:2].upper()
            random_number = random.randint(100, 999)
            self.sku = f"PR-{category_code}-{random_number}"
        super().save(*args, **kwargs)

    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    def __str__(self):
        return self.name
    

class StockMovement(models.Model):
    MOVEMENT_CHOICES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )

    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.movement_type} - {self.quantity}"

    
    

    


   
    
