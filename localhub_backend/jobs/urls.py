from django.urls import path
from .views import JobListCreateView, JobDetailView, JobApplicationView, CompanyListView

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/apply/', JobApplicationView.as_view(), name='job-apply'),
    path('companies/', CompanyListView.as_view(), name='company-list'),
]