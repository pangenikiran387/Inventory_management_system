from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from products.models import Supplier


# LIST
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/supplier_list.html', {
        'suppliers': suppliers
    })

# ADD
from django.shortcuts import render, redirect
from .models import Supplier
from .forms import SupplierForm

from django.shortcuts import render, redirect
from .models import Supplier
from .forms import SupplierForm
def add_supplier(request):
    if request.method == 'POST':
        print("POST HIT")   # ✅ check request

        form = SupplierForm(request.POST)

        if form.is_valid():
            supplier = form.save()
            print("SAVED:", supplier)   # ✅ check save
            return redirect('suppliers:supplier_list')
        else:
            print("ERRORS:", form.errors)   # ❌ check error

    else:
        form = SupplierForm()

    return render(request, 'suppliers/add_supplier.html', {'form': form})
# EDIT
def edit_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers:supplier_list')
    else:
        form = SupplierForm(instance=supplier) 

    return render(request, 'suppliers/edit_supplier.html', {'form': form})

# DELETE
def delete_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    supplier.delete()
    return redirect('suppliers:supplier_list')