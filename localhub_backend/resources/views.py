from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Resource, Rental, ResourceReview, Location
from .serializers import ResourceSerializer, RentalSerializer, ResourceReviewSerializer, LocationSerializer
from datetime import datetime

class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        filters = {
            'type__iexact': params.get('type'),
            'condition__iexact': params.get('condition'),
            'location__name__iexact': params.get('location')
        }
        queryset = queryset.filter(**{k: v for k, v in filters.items() if v})

        price_min = params.get('price_min')
        price_max = params.get('price_max')
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset

class ResourceDetailView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.AllowAny]

class ResourceRentalCreateView(generics.CreateAPIView):
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        resource_id = self.kwargs['pk']
        serializer.save(user=self.request.user, resource_id=resource_id)

class ResourceReviewCreateView(generics.CreateAPIView):
    serializer_class = ResourceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        resource_id = self.kwargs['pk']
        serializer.save(user=self.request.user, resource_id=resource_id)

class ResourceReviewListView(generics.ListAPIView):
    serializer_class = ResourceReviewSerializer

    def get_queryset(self):
        return ResourceReview.objects.filter(resource_id=self.kwargs['pk'])

class ResourceMapView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]

class ResourceAvailabilityView(APIView):
    def get(self, request, pk):
        try:
            resource = Resource.objects.get(pk=pk)
        except Resource.DoesNotExist:
            return Response({"error": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if not start or not end:
            return Response({"error": "Start and end dates required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        overlapping = Rental.objects.filter(
            resource=resource,
            start_date__lt=end_date,
            end_date__gt=start_date,
            status__in=['pending', 'approved']
        )

        is_available = not overlapping.exists()
        return Response({"available": is_available}, status=status.HTTP_200_OK)
