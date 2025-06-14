# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .paypal import PayPalClient
from .serializers import PaymentNotificationSerializer, TranslationSerializer, PaymentSerializer
from .models import Translation, Payment
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
import requests
import uuid

class CreatePayPalOrderView(APIView):
    def post(self, request):
        amount = request.data.get("amount")
        if not amount:
            return Response({"error": "Amount required"}, status=400)

        paypal = PayPalClient()
        order = paypal.create_order(amount)
        return Response(order)


class CapturePayPalOrderView(APIView):
    def post(self, request, order_id):
        paypal = PayPalClient()
        result = paypal.capture_order(order_id)
        return Response(result)


class TranslationListView(generics.ListAPIView):
    serializer_class = TranslationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        language = self.request.query_params.get('lang', 'en')
        return Translation.objects.filter(language_code=language)


@method_decorator(csrf_exempt, name='dispatch')
class InitiatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        amount = request.data.get('amount')
        gateway = request.data.get('gateway', 'telebirr')
        transaction_id = str(uuid.uuid4())

        if gateway == 'paypal':
            paypal = PayPalClient()
            try:
                order = paypal.create_order(amount)
            except Exception as e:
                return Response({"error": "PayPal error", "details": str(e)}, status=502)
            gateway_response = order
        else:
            try:
                response = requests.post("http://localhost:3001/api/order", json={
                    "title": "Payment from Django",
                    "amount": amount,
                    "transaction_id": transaction_id
                })
                response.raise_for_status()
                gateway_response = response.json()
            except Exception as e:
                return Response({"error": "Payment gateway error", "details": str(e)}, status=502)

        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            gateway=gateway,
            status='pending',
            transaction_id=transaction_id
        )

        return Response({
            "status": "initiated",
            "payment_id": payment.id,
            "transaction_id": transaction_id,
            "gateway_response": gateway_response
        }, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class VerifyPaymentView(generics.GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        payment_id = request.data.get('payment_id')
        success = request.data.get('success', False)

        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)

        payment.status = 'success' if success else 'failed'
        payment.save()
        return Response({'status': payment.status})


@method_decorator(csrf_exempt, name='dispatch')
class WebhookPaymentNotificationView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = PaymentNotificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        transaction_id = serializer.validated_data['transaction_id']
        new_status = serializer.validated_data['status']

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)

        payment.status = new_status
        payment.save()
        return Response({'status': 'updated'}, status=status.HTTP_200_OK)
