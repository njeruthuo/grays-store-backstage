from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from mpesa.views import stk_push, mpesa_callback

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/catalogue/', include('catalogue.urls')),
    path('api/user/', include('users.urls')),
    # path('payments/', include('payment.urls'))

    path('api/stk-push/', stk_push),
    path('callback/', mpesa_callback),

]+static(settings.STATIC_URL,
         document_root=settings.STATIC_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
