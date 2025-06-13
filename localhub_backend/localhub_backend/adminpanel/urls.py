from django.contrib import admin
from django.urls import path, include
from .views import AdminOverviewAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpanel/overview/', AdminOverviewAPIView.as_view(), name='admin-overview'),
]
