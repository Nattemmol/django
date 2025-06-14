from rest_framework import serializers
from .models import Report, ModerationLog

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['reported_by', 'created_at']


class ModerationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationLog
        fields = '__all__'
        read_only_fields = ['moderator', 'timestamp']