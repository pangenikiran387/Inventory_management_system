from django.urls import path, include
from products import views
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SupplierViewSet, ProductViewSet, StockMovementViewSet

# router = DefaultRouter()
# router.register('categories', CategoryViewSet)
# router.register('suppliers', SupplierViewSet)
# router.register('products', ProductViewSet)
# router.register('movements', StockMovementViewSet)
app_name = 'products'

urlpatterns = [
   path('add/', views.add_product, name='add_product'),
  
   path('', views.product_list, name='product_list'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),
   path('<int:product_id>/', views.product_detail, name='product-detail'),
   path('<int:product_id>/movement/', views.product_movement, name='product_movement'),
   path('products/edit/<int:id>/', views.edit_product, name='edit_product'),

   path('categories/', views.category_list, name='category_list'),
   path('categories/add/', views.add_category, name='add_category'),
   path('categories/edit/<int:id>/', views.edit_category, name='edit_category'),
   path('categories/delete/<int:id>/', views.delete_category, name='delete_category'),
]