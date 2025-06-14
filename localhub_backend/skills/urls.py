from django.urls import path
from .views import (
    SkillListCreateView, SkillDetailView,
    SkillReviewCreateView, SkillReviewListView,
    CategoryListView
)

urlpatterns = [
    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),
    path('skills/<int:pk>/review/', SkillReviewCreateView.as_view(), name='skill-review-create'),
    path('skills/<int:pk>/review/list/', SkillReviewListView.as_view(), name='skill-review-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]
