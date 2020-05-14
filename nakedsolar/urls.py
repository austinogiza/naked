
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from dispatch import receiver
from paystack import signals
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('', include('details.urls')),
    path('accounts/', include('allauth.urls')),
  # path('pay-with-paystack', include('paystack.urls')),
    path("paystack", include(('paystack.urls','paystack'),namespace='paystack')), 
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)