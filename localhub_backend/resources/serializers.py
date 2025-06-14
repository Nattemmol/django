from rest_framework import serializers
from .models import Resource, Rental, ResourceReview, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'

class ResourceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceReview
        fields = '__all__'
