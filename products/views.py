from http.client import HTTPResponse
from pyexpat.errors import messages
from unicodedata import category

from django.shortcuts import redirect, render
from django.db.models import F
from accounts.auth import is_admin, is_staff
from rest_framework import viewsets
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required



from .models import Products, Category, Supplier, StockMovement   
from .forms import ProductForm
from .forms import CategoryForm
from .serializers import (
    CategorySerializer,
    SupplierSerializer,
    ProductSerializer,
    StockMovementSerializer
)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        low_stock = self.request.query_params.get('low_stock')

        if low_stock == 'true':
            queryset = queryset.filter(quantity__lte=F('low_stock_threshold'))

        return queryset


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer

    def perform_create(self, serializer):
        movement = serializer.save()
        product = movement.product

        if movement.movement_type == 'IN':
            product.quantity += movement.quantity
        elif movement.movement_type == 'OUT':
            product.quantity -= movement.quantity

        product.save()

from django.shortcuts import render
from .models import Category


def category_list(request):
    categories = Category.objects.all()
    print(categories)

    return render(request, 'products/category_list.html', {
        'categories': categories
    })

def add_category(request):
    if request.method == 'POST':
        Category.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('category_list')

    return render(request, 'products/add_category.html')
   

from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import CategoryForm

def edit_category(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('products:category_list')
    else:
        form = CategoryForm(instance=category)  

    return render(request, 'products/edit_category.html', {'form': form})
    
def delete_category(request,id):
    object=get_object_or_404(Category,id=id)

    object.delete()
    return redirect('products:category_list')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})

@login_required
def product_list(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if not (is_admin(request.user) or is_staff(request.user)):
        return redirect('accounts:homepage')
    products=Products.objects.all()
    return render(request,'products/product_list.html',{'products':products})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, StockMovement
from django.contrib.auth.decorators import login_required, permission_required

def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    movements = product.movements.all().order_by('-created_at')

    return render(request, 'products/product_detail.html', {
        'product': product,
        'movements': movements
    })

@login_required
def delete_product(request,id):
    object=get_object_or_404(Products,id=id)

    object.delete()
    return redirect('products:product_list')

@login_required
def edit_product(request, id):
    product = get_object_or_404(Products, id=id)

    if request.method == 'POST':
        product.name = request.POST.get('name')  
        product.sku = request.POST.get('sku')
        product.price = request.POST.get('price')
        product.save()

        return redirect('products:product_list')  

    return render(request, 'products/edit_product.html', {'product': product})
 

from .models import Products, StockMovement

def product_movement(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if request.method == 'POST':
        movement_type = request.POST.get('movement_type')
        quantity = int(request.POST.get('quantity'))

        if movement_type == 'IN':
            product.quantity += quantity
        elif movement_type == 'OUT':
            if product.quantity < quantity:
                return HTTPResponse("Not enough stock")
            product.quantity -= quantity

        product.save()

       
        StockMovement.objects.create(
            product=product,
            movement_type=movement_type,
            quantity=quantity
        )

        return redirect('products:product_movement', product_id=product.id)

    movements = product.movements.all().order_by('-created_at')

    return render(request, 'products/product_movement.html', {
        'product': product,
        'movements': movements
    })