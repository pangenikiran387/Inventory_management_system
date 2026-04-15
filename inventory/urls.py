from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # homepage ONLY
    path('', home_view, name='home'),

    # apps
    path('dashboard/', include('dashboard.urls')),
    path('products/', include('products.urls')),
    path('suppliers/', include(('suppliers.urls', 'suppliers'), namespace='suppliers')),
    path('accounts/', include('accounts.urls')),
    path('stock/', include('stock.urls')),
    path('purchases/', include('purchases.urls')),
    path('sales/', include('sales.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)