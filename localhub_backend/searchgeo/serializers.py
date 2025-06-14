from rest_framework import serializers
from .models import SearchQuery, GeoLocation

class SearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchQuery
        fields = '__all__'

class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = '__all__'
