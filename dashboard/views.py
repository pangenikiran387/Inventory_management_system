import json
from django.shortcuts import render, redirect
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required

from products.models import Products, StockMovement, Category
from suppliers.models import Supplier


@login_required
def dashboard(request):

    # 🔐 Only admin allowed
    if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
        return redirect('sales:pos')

    products = Products.objects.all()[:5]

    # ===== KPI =====
    total_products = Products.objects.count()

    stock_value = Products.objects.aggregate(
        total_value=Sum(F('quantity') * F('price'))
    )['total_value'] or 0

    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()

    low_stock = Products.objects.filter(
        quantity__lte=F('low_stock_threshold'),
        quantity__gt=0
    ).count()

    out_of_stock = Products.objects.filter(quantity=0).count()

    suppliers = Supplier.objects.all()[:5]

    # ===== LAST 7 DAYS =====
    last_7_days = now() - timedelta(days=7)

    movements = StockMovement.objects.filter(
        created_at__gte=last_7_days
    ).order_by('created_at')

    dates, stock_in, stock_out = [], [], []

    for m in movements:
        dates.append(m.created_at.strftime("%d-%m"))

        if m.movement_type == 'IN':
            stock_in.append(m.quantity)
            stock_out.append(0)
        else:
            stock_in.append(0)
            stock_out.append(m.quantity)

    # ===== MONTHLY =====
    monthly = (
        StockMovement.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month', 'movement_type')
        .annotate(total=Sum('quantity'))
        .order_by('month')
    )

    months, in_data, out_data = [], [], []

    for m in monthly:
        label = m['month'].strftime("%b")

        if label not in months:
            months.append(label)
            in_data.append(0)
            out_data.append(0)

        idx = months.index(label)

        if m['movement_type'] == 'IN':
            in_data[idx] += m['total']
        else:
            out_data[idx] += m['total']

    # ===== CATEGORY PIE =====
    categories = Category.objects.annotate(
        total=Sum('products__quantity')
    )

    cat_labels = [c.name for c in categories]
    cat_data = [c.total or 0 for c in categories]

    return render(request, 'dashboard/index.html', {
        'products': products,

        'total_products': total_products,
        'stock_value': stock_value,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'suppliers': suppliers,

        'dates_json': json.dumps(dates),
        'stock_in_json': json.dumps(stock_in),
        'stock_out_json': json.dumps(stock_out),

        'months': json.dumps(months),
        'in_data': json.dumps(in_data),
        'out_data': json.dumps(out_data),

        'cat_labels': json.dumps(cat_labels),
        'cat_data': json.dumps(cat_data),
    })