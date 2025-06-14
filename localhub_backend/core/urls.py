from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, ProfileView,
    NearbyUsersView, RoleListView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/nearby/', NearbyUsersView.as_view(), name='nearby-users'),
    path('roles/', RoleListView.as_view(), name='roles'),
]

 #   "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0OTc1ODY0NiwiaWF0IjoxNzQ5NjcyMjQ2LCJqdGkiOiI4MmEwNzllZGJhZGY0MDEzYTA2ZmNhYTI3YjdmYmJlNyIsInVzZXJfaWQiOjZ9.Mts3dZjATSWVzbYRdbyoeR4xgBQi9xn7FDDD6GMml0s",
 #   "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5NjczMTQ2LCJpYXQiOjE3NDk2NzIyNDYsImp0aSI6IjZjMDYyYTIwNmQ3ODQ1NDFhNjNkMzc0YTNjYzA3Y2VhIiwidXNlcl9pZCI6Nn0.kiUAYmQm9H-Na_XagMMBDII_QNxJKCk5alp59j9B57U"