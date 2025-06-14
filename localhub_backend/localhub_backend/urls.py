from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.static import serve

# DRF-YASG imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view setup
schema_view = get_schema_view(
    openapi.Info(
        title="LocalHub API Documentation",
        default_version='v1',
        description="API documentation for LocalHub backend project.",
        terms_of_service="https://www.yourdomain.com/terms/",
        contact=openapi.Contact(email="support@yourdomain.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('skills/', include('skills.urls')),
    path('resources/', include('resources.urls')),
    path('jobs/', include('jobs.urls')),
    path('learning/', include('learning.urls')),
    path('searchgeo/', include('searchgeo.urls')),
    path('communication/', include('communication.urls')),
    path('moderation/', include('moderation.urls')),
    path('localization/', include('localization.urls')),
    path('partnerships/', include('partnerships.urls')),
    path('adminpanel/', include('adminpanel.urls')),

    # DRF-YASG Documentation URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
