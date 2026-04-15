from django.shortcuts import get_object_or_404, redirect, render



from products.models import Products, StockMovement

def product_movement(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.product = product

          
            if movement.movement_type == 'IN':
                product.quantity += movement.quantity
            else:
                product.quantity -= movement.quantity

            product.save()

           
            movement.balance = product.quantity
            movement.user = request.user.username if request.user.is_authenticated else "Admin"

            movement.save()

            return redirect('products:product-detail', product_id=product.id)
    else:
        form = StockMovementForm()

    return render(request, 'products/product_movement.html', {
        'form': form,
        'product': product
    })

def stock_dashboard(request):
    stocks = StockMovement.objects.all().order_by('-created_at')

    return render(request, 'stock/stock_list.html', {
        'stocks': stocks
    })

from django.shortcuts import render, redirect
from .forms import StockMovementForm


def add_stock(request):
    error = None 

    if request.method == 'POST':
        form = StockMovementForm(request.POST)

        if form.is_valid():
            stock = form.save(commit=False)
            product = stock.product

          
            if stock.movement_type == 'IN':
                product.quantity += stock.quantity

          
            elif stock.movement_type == 'OUT':
                if product.quantity < stock.quantity:
                    error = 'Not enough stock available'
                    return render(request, 'stock/add_stock.html', {
                        'form': form,
                        'error': error
                    })

                product.quantity -= stock.quantity

            
            product.save()
            stock.save()

            return redirect('stock:stock_list')

    else:
        form = StockMovementForm()

    return render(request, 'stock/add_stock.html', {
        'form': form,
        'error': error
    })


def stock_in(product, quantity):
    product.quantity += quantity
    product.save()

    StockMovement.objects.create(
        product=product,
        movement_type='IN',
        quantity=quantity,
        # transaction_type=StockTransaction.STOCK_IN,
        # quantity=quantity
    )
def stock_out(product, quantity):
    if product.quantity < quantity:
        raise ValueError("Not enough stock")

    product.quantity -= quantity
    product.save()

    StockMovement.objects.create(
        product=product,
        movement_type='OUT',
        quantity=quantity
    )


