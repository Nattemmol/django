# core/paypal.py
import requests
import json
from django.conf import settings
from base64 import b64encode

class PayPalClient:
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.secret = settings.PAYPAL_SECRET
        self.base_url = "https://api-m.sandbox.paypal.com"  # Change to live endpoint in production
        self.token = self.get_access_token()

    def get_access_token(self):
        url = f"{self.base_url}/v1/oauth2/token"
        auth = b64encode(f"{self.client_id}:{self.secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        res = requests.post(url, headers=headers, data=data)
        return res.json().get("access_token")

    def create_order(self, amount):
        url = f"{self.base_url}/v2/checkout/orders"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "intent": "CAPTURE",
            "purchase_units": [{"amount": {"currency_code": "USD", "value": str(amount)}}]
        }
        res = requests.post(url, headers=headers, data=json.dumps(data))
        return res.json()

    def capture_order(self, order_id):
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        res = requests.post(url, headers=headers)
        return res.json()
