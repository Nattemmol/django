from rest_framework import generics, permissions
from .models import Skill, SkillReview, Category
from .serializers import SkillSerializer, SkillReviewSerializer, CategorySerializer

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SkillReviewCreateView(generics.CreateAPIView):
    serializer_class = SkillReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, skill_id=self.kwargs['pk'])

class SkillReviewListView(generics.ListAPIView):
    serializer_class = SkillReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SkillReview.objects.filter(skill_id=self.kwargs['pk'])

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
