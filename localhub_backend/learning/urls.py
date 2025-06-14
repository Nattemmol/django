from django.urls import path
from .views import (
    CourseListCreateView,
    CourseDetailView,
    CourseProgressView,
    CertificateView,
    CertificateDownloadView,
    QuizListView,
    AssignmentListView,
    AssignmentSubmissionView
)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/progress/', CourseProgressView.as_view(), name='course-progress'),
    path('courses/<int:pk>/certificate/', CertificateView.as_view(), name='course-certificate'),
    path('courses/<int:pk>/certificate/download/', CertificateDownloadView.as_view(), name='certificate-download'),
    path('courses/<int:pk>/quizzes/', QuizListView.as_view(), name='course-quizzes'),
    path('courses/<int:pk>/assignments/', AssignmentListView.as_view(), name='course-assignments'),
    path('assignments/<int:pk>/submit/', AssignmentSubmissionView.as_view(), name='assignment-submit'),
]
