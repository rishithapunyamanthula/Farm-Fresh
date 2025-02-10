from django.contrib import admin
from django.urls import path, include
from customers import views as customer_views
from sellers import views as seller_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', customer_views.home, name='home'),  # Home page
    path('customer/', include('customers.urls')),
    path('seller/', include('sellers.urls')),
    path('logout/', customer_views.custom_logout_view, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
