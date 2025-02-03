from django.urls import path
from .views import (
    CategoryListCreateView,
    EventListCreateView,
    EventDetailView,
    GuestListCreateView,
    UserListCreateView,
    UserDetailView,
    EventGuestListView,
    AddGuestToEventView,
    LoginView,
    LogoutView,
    RegisterView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),

    # Events
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<str:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<str:event_id>/guests/', EventGuestListView.as_view(), name='event-guests'),
    path('events/<str:event_id>/guests/add/', AddGuestToEventView.as_view(), name='add-guest-to-event'),

    # Guests
    path('guests/', GuestListCreateView.as_view(), name='guest-list-create'),

    # Users
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
]
