from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import SalesItem, SalesOrder
from products.models import Products, StockMovement
from accounts.models import Customer

def confirm_sale(request, id):
    sale = get_object_or_404(SalesOrder, id=id)

    sale.payment_status = 'PAID'
    sale.save() 

    return redirect('sales:sales_invoice', id=sale.id)

def sales_detail(request, id):
    sale = get_object_or_404(SalesOrder, id=id)
    items = sale.items.all()

    total = sum(item.quantity * item.selling_price for item in items)
    profit = 0

    for item in items:
        cost = item.product.cost_price  # your cost price field
        from decimal import Decimal

        profit += (Decimal(item.selling_price) - cost) * item.quantity

    return render(request, 'sales/sales_detail.html', {
        'sale': sale,
        'items': items,
        'total': total
    })

def sales_list(request):
    sales = SalesOrder.objects.all().order_by('-created_at')

    return render(request, 'sales/sales_list.html', {
        'sales': sales
    })
from django.shortcuts import render, get_object_or_404
from .models import SalesOrder

def sales_invoice(request, id):
    sale = get_object_or_404(SalesOrder, id=id)
    items = sale.items.all()

    total = sum(i.total() for i in items)

    return render(request, 'sales/invoice.html', {
        'sale': sale,
        'items': items,
        'total': total
    })


def pos_view(request):
    products = Products.objects.all()
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for pid, qty in cart.items():
        product = Products.objects.get(id=pid)
        item_total = product.price * qty
        total += item_total

        cart_items.append({
            'product': product,
            'qty': qty,
            'total': item_total
        })

    return render(request, 'sales/pos.html', {
        'products': products,
        'cart_items': cart_items,
        'total': total
    })

def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    cart[str(id)] = cart.get(str(id), 0) + 1

    request.session['cart'] = cart
    return redirect('sales:pos')

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('sales:pos')

def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('sales:pos')

    customer = Customer.objects.first()  # later improve

    payment_method = request.POST.get('payment_method', 'COD')

    sale = SalesOrder.objects.create(
        customer=customer,
        payment_method=payment_method,
        payment_status='PAID' if payment_method == 'COD' else 'PENDING'
    )

    for pid, qty in cart.items():
        product = Products.objects.get(id=pid)

        SalesItem.objects.create(
            sales=sale,
            product=product,
            quantity=qty,
            selling_price=product.price
        )

        # reduce stock
        product.quantity -= qty
        product.save()

    request.session['cart'] = {}

    return redirect('sales:sales_invoice', id=sale.id)

def increase_qty(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1

    request.session['cart'] = cart
    return redirect('sales:pos')

def decrease_qty(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] -= 1

        if cart[str(id)] <= 0:
            del cart[str(id)]

    request.session['cart'] = cart
    return redirect('sales:pos')

def remove_item(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart
    return redirect('sales:pos')
import uuid
import hmac
import hashlib
import base64
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import SalesOrder


def generate_signature(secret_key, message):
    key = bytes(secret_key, 'utf-8')
    message = bytes(message, 'utf-8')

    hmac_obj = hmac.new(key, message, hashlib.sha256)
    signature = base64.b64encode(hmac_obj.digest()).decode()

    return signature


class EsewaView(View):
    def get(self, request, id):
        sale = get_object_or_404(SalesOrder, id=id)

        total = sum(item.total() for item in sale.items.all())

        transaction_uuid = str(uuid.uuid4())

        secret_key = "8gBm/:&EnhH.1/q"  # test key

       
        message = f"total_amount={total},transaction_uuid={transaction_uuid},product_code=EPAYTEST"

        signature = generate_signature(secret_key, message)

        context = {
            "sale": sale,
            "total": total,
            "transaction_uuid": transaction_uuid,
            "signature": signature,
        }

        return render(request, "sales/esewaform.html", context)