from django.db import models
from django.conf import settings

class Translation(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()
    language_code = models.CharField(max_length=10)

    class Meta:
        unique_together = ('key', 'language_code')

    def __str__(self):
        return f"{self.key} ({self.language_code})"

class Payment(models.Model):
    GATEWAY_CHOICES = [
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('cbebirr', 'CBE Birr'),
        ('telebirr', 'Telebirr'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
