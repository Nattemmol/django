from rest_framework import serializers
from .models import NGOPartner, BusinessAd

class NGOPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGOPartner
        fields = '__all__'

class BusinessAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAd
        fields = '__all__'
