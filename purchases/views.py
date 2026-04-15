from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import PurchaseOrder, PurchaseItem
from products.models import Products, StockMovement

from suppliers.models import Supplier

def create_purchase(request):
    suppliers = Supplier.objects.all()
    products = Products.objects.all()

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")

        purchase = PurchaseOrder.objects.create(
            supplier_id=supplier_id
        )

        product_ids = request.POST.getlist("product")
        quantities = request.POST.getlist("quantity")
        prices = request.POST.getlist("cost_price")

        for i in range(len(product_ids)):
            product = Products.objects.get(id=product_ids[i])

            qty = int(quantities[i])
            price = float(prices[i])

            PurchaseItem.objects.create(
                purchase=purchase,
                product=product,
                quantity=qty,
                cost_price=price
            )

        return redirect("purchase:purchase_list")

    return render(request, "purchase/create_purchase.html", {
        "suppliers": suppliers,
        "products": products
    })


def confirm_purchase(request, id):
    purchase = get_object_or_404(PurchaseOrder, id=id)

    if purchase.is_confirmed:
        return redirect("purchase:purchase_list")

    for item in purchase.items.all():
        product = item.product

        # 🔥 Increase stock
        product.quantity += item.quantity
        product.save()

        # 🔥 Stock movement log
        StockMovement.objects.create(
            product=product,
            movement_type='IN',
            quantity=item.quantity,
            remark=f"Purchase PO-{purchase.id}"
        )

    purchase.is_confirmed = True
    purchase.save()

    return redirect("purchase:purchase_list")

def purchase_list(request):
    purchases = PurchaseOrder.objects.all().order_by('-created_at')

    return render(request, "purchases/purchase_list.html", {
        "purchases": purchases
    })

def purchase_detail(request, id):
    purchase = get_object_or_404(PurchaseOrder, id=id)
    items = purchase.items.all()

    total = sum(item.quantity * item.cost_price for item in items)

    return render(request, 'purchases/purchase_detail.html', {
        'purchase': purchase,
        'items': items,
        'total': total
    })

def purchase_invoice(request, id):
    purchase = get_object_or_404(PurchaseOrder, id=id)
    items = purchase.items.all()

    total = sum(item.quantity * item.cost_price for item in items)

    return render(request, 'purchases/invoice.html', {
        'purchase': purchase,
        'items': items,
        'total': total
    })