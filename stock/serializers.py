from itertools import product

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (Category,Supplier,Product,Stocktransaction,PurchaseOrder,PurchaseOrderItem,SaleOrder,SaleOrderItem)

#auth
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.charField(write_only=True,min_lenght=6)

    class Meta:
        model=User
        fields=['id','username','email','password']

    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)

        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fieds=['id','username','email']

class CategorySerializer(serializers.ModelSerializer):
    product_count=serializers.SerializerMethondField()

    class Meta:
        model=Supplier
        fields='__all__'
class ProductSerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(source='category.name',read_only=True)
    supplier_name=serializers.CharField(Source='supplier.name',read_only=True)
    is_low_stock=serializers.ReadonlyFields()
    stock_value=serializers.Readonly()

    class Meta:
        model=Product
        fields='__all__'
    def create(self,validaed_data):
        product=validaed_data['product']
        quantity=validaed_data['quantity']
        t_type=validaed_data['transaction_type']

        if type=='IN':
            product.quantity_in_stock+=quantity
        elif t_type =='OUT':
            if product.quantity_in_stock <quantity:

                raise serializers .validationError(
            {"quantity":"Insufficient stock available"}
        )
            product.quantity_in_stock=quantity
            product.save()
        return super().create(validaed_data)
    
#purchaseorder

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    total_price=serializers.ReadOnly()

    class Meta:
        model=PurchaseOrderItem
        fields='__all__'
class PurchaseOrderSerializer(serializers.ModelSerializer):
    items=PurchaseOrderItemSerializer(many=True,read_only=True)
    Supplier_name=serializers.CharField(source='supplier.name',read_only=True)

    class Meta:
        model=PurchaseOrder
        fields='__all__'
        read_only_fields=['created-at','total_amount']

#sales order

class SalesOrderItemSerializer(serializers.ModelSerializer):
    total-price=serializers.ReadOnlyField()

    class Meta:
        model=SaleOrderItem
        fields='__all__'

class SalesOrderSerializer(serializers.ModelSerializer):
    items=SalesOrderItemSerializer(many=True,read_only=True)

    class Meta:
        model=SaleOrder
        fields='__all__'
        read_only_fields=['created_by','total_amount']


