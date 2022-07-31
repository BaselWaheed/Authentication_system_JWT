from django.contrib import admin
from django.urls import path , include 
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="API ",
      default_version='v1',
      description="API for Authentication",
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(name='basel waheed ' ,email="baselwaheed66@gmail.com"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)




urlpatterns = [
    path('baselwaheed/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('social_auth/', include('social_auth.urls')),
    path('event/', include('event.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)