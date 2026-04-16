from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path('<int:id>/', views.sales_detail, name='sales_detail'),
    path('confirm/<int:id>/', views.confirm_sale, name='confirm_sale'),
    path('', views.sales_list, name='sales_list'),
    path('invoice/<int:id>/', views.sales_invoice, name='sales_invoice'),
    path('pos/', views.pos_view, name='pos'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('increase/<int:id>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:id>/', views.decrease_qty, name='decrease_qty'),
    path('remove/<int:id>/', views.remove_item, name='remove_item'),
    path('esewa/<int:id>/', views.esewa_form, name='esewa_form'),
    path('esewa-verify/', views.esewa_verify, name='esewa_verify'),
]