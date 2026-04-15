from django.urls import path
from . import views
app_name='stock'

urlpatterns = [
    path('', views.stock_dashboard, name='stock_list'),
    path('add/', views.add_stock, name='add_stock'),
]