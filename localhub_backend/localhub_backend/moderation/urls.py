from django.urls import path
from .views import CreateReportView, AdminReportListView, ModerationActionView

urlpatterns = [
    path('report/', CreateReportView.as_view(), name='create-report'),
    path('admin/reports/', AdminReportListView.as_view(), name='admin-report-list'),
    path('admin/action/', ModerationActionView.as_view(), name='moderation-action'),
]
