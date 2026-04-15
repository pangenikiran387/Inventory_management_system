from django.urls import path
from . import views

app_name = "purchases"

urlpatterns = [
    path('', views.purchase_list, name='purchase_list'),
    path('create/', views.create_purchase, name='create_purchase'),
    path('confirm/<int:id>/', views.confirm_purchase, name='confirm_purchase'),
    path('<int:id>/', views.purchase_detail, name='purchase_detail'), 
    path('invoice/<int:id>/', views.purchase_invoice, name='purchase_invoice'),
]