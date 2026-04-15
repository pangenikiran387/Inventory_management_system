# accounts/urls.py

from django.urls import path
from . import views   # ✅ CORRECT (use local app views)

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='homepage'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]