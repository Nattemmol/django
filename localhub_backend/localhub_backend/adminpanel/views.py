from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Analytics, SupportTicket
from moderation.models import Report
from .serializers import AnalyticsSerializer

class AdminOverviewAPIView(APIView):
    def get(self, request):
        latest_analytics = Analytics.objects.order_by('-date').first()
        open_tickets = SupportTicket.objects.filter(status='open').count()
        unresolved_tickets = SupportTicket.objects.exclude(status='resolved').count()
        pending_reports = Report.objects.count()

        data = {
            "latest_analytics": AnalyticsSerializer(latest_analytics).data if latest_analytics else None,
            "open_tickets": open_tickets,
            "unresolved_tickets": unresolved_tickets,
            "pending_reports": pending_reports,
        }
        return Response(data)
