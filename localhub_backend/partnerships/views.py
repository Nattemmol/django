from rest_framework import generics, permissions
from .models import NGOPartner, BusinessAd
from .serializers import NGOPartnerSerializer, BusinessAdSerializer

class NGOPartnerListCreateView(generics.ListCreateAPIView):
    queryset = NGOPartner.objects.all()
    serializer_class = NGOPartnerSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class BusinessAdListCreateView(generics.ListCreateAPIView):
    queryset = BusinessAd.objects.all()
    serializer_class = BusinessAdSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
