from django.urls import path
from .views import (
    TranslationListView,
    InitiatePaymentView,
    VerifyPaymentView,
    WebhookPaymentNotificationView,
    CreatePayPalOrderView,
    CapturePayPalOrderView
)

urlpatterns = [
    # i18n
    path('i18n/', TranslationListView.as_view(), name='i18n'),

    # General Payment Handling
    path('payment/initiate/', InitiatePaymentView.as_view(), name='payment-initiate'),
    path('payment/verify/', VerifyPaymentView.as_view(), name='payment-verify'),
    path('payment/webhook/', WebhookPaymentNotificationView.as_view(), name='payment-webhook'),

    # PayPal Integration
    path('payment/create/', CreatePayPalOrderView.as_view(), name='paypal-create'),
    path('payment/capture/<str:order_id>/', CapturePayPalOrderView.as_view(), name='paypal-capture'),
]
