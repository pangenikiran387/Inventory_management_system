import json
import hmac
import hashlib
import base64
import uuid

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

    customer_name = request.POST.get('customer_name')
    payment_method = request.POST.get('payment_method')

    sale = SalesOrder.objects.create(
        
        customer_name=customer_name,
        payment_method=payment_method,
        payment_status='PENDING'
    )

    for pid, qty in cart.items():
        product = Products.objects.get(id=pid)

        SalesItem.objects.create(
            sales=sale,
            product=product,
            quantity=qty,
            selling_price=product.price
        )

        product.quantity -= qty
        product.save()

    request.session['cart'] = {}

    # ✅ COD → direct invoice
    if payment_method == 'COD':
        sale.payment_status = 'PAID'
        sale.save()
        return redirect('sales:sales_invoice', id=sale.id)

    # ✅ eSewa → redirect to payment
    else:
        return redirect('sales:esewa_form', id=sale.id)

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

def generate_signature(secret_key, message):
    key = bytes(secret_key, 'utf-8')
    message = bytes(message, 'utf-8')

    hmac_obj = hmac.new(key, message, hashlib.sha256)
    signature = base64.b64encode(hmac_obj.digest()).decode()

    return signature


def esewa_verify(request):
    data = request.GET.get('data')

    if not data:
        return redirect('sales:pos')

    try:
        decoded_data = base64.b64decode(data).decode('utf-8')
        map_data = json.loads(decoded_data)
    except:
        return redirect('sales:pos')

    transaction_uuid = map_data.get('transaction_uuid')
    status = map_data.get('status')
    total_amount = map_data.get('total_amount')
    product_code = map_data.get('product_code')
    signed_field_names = map_data.get('signed_field_names')
    received_signature = map_data.get('signature')

    # Extract sale id from transaction_uuid
    try:
        sale_id = int(transaction_uuid.split("-")[1])
    except:
        return redirect('sales:pos')

    sale = get_object_or_404(SalesOrder, id=sale_id)

    # Calculate expected total
    expected_total = sum(item.total() for item in sale.items.all())

    # Verify amounts match
    if float(total_amount) != expected_total:
        sale.payment_status = 'FAILED'
        sale.save()
        return redirect('sales:pos')

    # Verify signature
    secret_key = "8gBm/:&EnhH.1/q"
    # The signed_field_names in response tells us which fields to use for verification
    # From docs: transaction_code,status,total_amount,transaction_uuid,product_code,signed_field_names
    message = f"transaction_code={map_data.get('transaction_code')},status={status},total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code},signed_field_names={signed_field_names}"
    expected_signature = generate_signature(secret_key, message)

    if received_signature != expected_signature:
        # Signature verification failed
        sale.payment_status = 'FAILED'
        sale.save()
        return redirect('sales:pos')

    if status == 'COMPLETE':
        sale.payment_status = 'PAID'
        sale.transaction_id = map_data.get('transaction_code')
        sale.save()
        return redirect('sales:sales_invoice', id=sale.id)
    else:
        sale.payment_status = 'FAILED'
        sale.save()
        return redirect('sales:pos')


def esewa_form(request, id):
    sale = get_object_or_404(SalesOrder, id=id)
    items = sale.items.all()
    total = sum(i.total() for i in items)

    transaction_uuid = f"ORDER-{sale.id}-{uuid.uuid4().hex[:12]}"
    sale.transaction_uuid = transaction_uuid
    sale.save()

    secret_key = "8gBm/:&EnhH.1/q"
    message = f"total_amount={total},transaction_uuid={transaction_uuid},product_code=EPAYTEST"
    signature = generate_signature(secret_key, message)

    context = {
        'sale': sale,
        'total': total,
        'transaction_uuid': transaction_uuid,
        'signature': signature,
    }

    return render(request, 'sales/esewaform.html', context)