from django.db import models

# Create your models here.
from django.db import models
from core.models import User

class Analytics(models.Model):
    date = models.DateField()
    active_users = models.IntegerField()
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    new_listings = models.IntegerField()
    sessions = models.IntegerField()

    def __str__(self):
        return f"Analytics for {self.date}"

class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket #{self.pk} - {self.user.username}"
