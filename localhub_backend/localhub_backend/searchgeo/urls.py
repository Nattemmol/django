from django.urls import path
from .views import SearchView, NearbySearchView, AdvancedSearchView

urlpatterns = [
    path('search/', SearchView.as_view()),
    path('search/nearby/', NearbySearchView.as_view()),
    path('search/advanced/', AdvancedSearchView.as_view()),
]
