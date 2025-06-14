from rest_framework import serializers
from .models import Analytics, SupportTicket

class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = '__all__'

class SupportTicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = SupportTicket
        fields = '__all__'
