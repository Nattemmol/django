from django.contrib import admin
from .models import NGOPartner, BusinessAd

@admin.register(NGOPartner)
class NGOPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')

@admin.register(BusinessAd)
class BusinessAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'business_name', 'valid_until')
    list_filter = ('valid_until',)
