from rest_framework import generics, permissions
from .models import Report, ModerationLog
from .serializers import ReportSerializer, ModerationLogSerializer

class CreateReportView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)


class AdminReportListView(generics.ListAPIView):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAdminUser]


class ModerationActionView(generics.CreateAPIView):
    serializer_class = ModerationLogSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(moderator=self.request.user)