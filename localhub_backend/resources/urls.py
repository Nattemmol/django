from django.urls import path
from .views import (
    ResourceListCreateView,
    ResourceDetailView,
    ResourceRentalCreateView,
    ResourceReviewCreateView,
    ResourceReviewListView,
    ResourceMapView,
    ResourceAvailabilityView
)

urlpatterns = [
    path('resources/', ResourceListCreateView.as_view(), name='resource-list-create'),
    path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource-detail'),
    path('resources/<int:pk>/rent/', ResourceRentalCreateView.as_view(), name='resource-rent'),
    path('resources/<int:pk>/review/', ResourceReviewCreateView.as_view(), name='resource-review-create'),
    path('resources/<int:pk>/reviews/', ResourceReviewListView.as_view(), name='resource-review-list'),
    path('resources/map/', ResourceMapView.as_view(), name='resource-map'),
    path('resources/<int:pk>/availability/', ResourceAvailabilityView.as_view(), name='resource-availability'),
]
