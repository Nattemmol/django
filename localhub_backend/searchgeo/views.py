from jobs.models import Job
from jobs.serializers import JobSerializer
from resources.models import Resource
from resources.serializers import ResourceSerializer
from skills.models import Skill
from skills.serializers import SkillSerializer
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import *
from .serializers import *
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c

class SearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '')
        filters = request.query_params.get('filters')

        # Log the query
        SearchQuery.objects.create(user=request.user, query=query, filters=filters)

        results = {}

        if query:
            skill_qs = Skill.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
            job_qs = Job.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(company__icontains=query))
            resource_qs = Resource.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query))

            results['skills'] = SkillSerializer(skill_qs, many=True).data
            results['jobs'] = JobSerializer(job_qs, many=True).data
            results['resources'] = ResourceSerializer(resource_qs, many=True).data
        else:
            results['message'] = "No query provided."

        return Response(results)

class NearbySearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_location = GeoLocation.objects.filter(user=request.user).last()
        if not user_location:
            return Response({"error": "User location not found"}, status=404)

        lat1, lon1 = user_location.lat, user_location.long
        radius_km = float(request.query_params.get("radius", 5))

        nearby_users = []
        for loc in GeoLocation.objects.exclude(user=request.user):
            distance = haversine(lat1, lon1, loc.lat, loc.long)
            if distance <= radius_km:
                nearby_users.append(loc)

        serializer = GeoLocationSerializer(nearby_users, many=True)
        return Response(serializer.data)

class AdvancedSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("query")
        lat = request.query_params.get("lat")
        long = request.query_params.get("long")
        radius_km = float(request.query_params.get("radius", 5))

        geo_filter_users = None
        if lat and long:
            lat = float(lat)
            long = float(long)
            geo_filter_users = []

            for loc in GeoLocation.objects.all():
                if haversine(lat, long, loc.lat, loc.long) <= radius_km:
                    geo_filter_users.append(loc.user_id)

        # Query the SearchQuery log for user's own history or all matching users
        search_qs = SearchQuery.objects.filter(user=request.user)
        if query:
            search_qs = search_qs.filter(query__icontains=query)

        if geo_filter_users:
            search_qs = search_qs.filter(user_id__in=geo_filter_users)

        serializer = SearchQuerySerializer(search_qs, many=True)
        return Response(serializer.data)
