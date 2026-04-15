from django.urls import path
from . import views
from suppliers.models import Supplier

app_name='suppliers'

urlpatterns = [
    path('add/', views.add_supplier, name='add_supplier'),
    path('', views.supplier_list, name='supplier_list'),
    path('edit/<int:id>/', views.edit_supplier, name='edit_supplier'),
    path('delete/<int:id>/', views.delete_supplier, name='delete_supplier'),
]