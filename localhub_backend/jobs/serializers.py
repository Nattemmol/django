from rest_framework import serializers
from .models import Job, Application, Company

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['user', 'job', 'status']

    def validate_cv(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError("CV file size should not exceed 5MB.")
        if not value.name.endswith(('.pdf', '.doc', '.docx')):
            raise serializers.ValidationError("Only PDF, DOC, and DOCX files are allowed.")
        return value

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
