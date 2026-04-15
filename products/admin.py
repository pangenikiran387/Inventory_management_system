from django.contrib import admin
from .models import StockMovement

from .models import Products,Category,Supplier

# admin.site.register(Category)
# admin.site.register(Products)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display=('id','name','email','phone')
    search_fields=('name','email','phone',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','name','description')
    search_fields=('name',)

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','name','category','supplier','price','quantity','image','sku')

    list_filter=('category','supplier')
    search_fields=('name',)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__name',)
    ordering = ('-created_at',)

