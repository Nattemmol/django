from django.urls import path
from .views import NGOPartnerListCreateView, BusinessAdListCreateView

urlpatterns = [
    path('partners/', NGOPartnerListCreateView.as_view(), name='ngo-partners'),
    path('ads/', BusinessAdListCreateView.as_view(), name='business-ads'),
]
