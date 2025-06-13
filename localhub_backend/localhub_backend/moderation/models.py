from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Report(models.Model):
    REASON_CHOICES = [
        ("inappropriate", "Inappropriate"),
        ("spam", "Spam"),
        ("abuse", "Abuse"),
        ("other", "Other"),
    ]

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_received')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'content_id')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reported_by} on {self.content_object}"  


class ModerationLog(models.Model):
    ACTION_CHOICES = [
        ("warned", "Warned"),
        ("banned", "Banned"),
        ("content_deleted", "Content Deleted"),
        ("no_action", "No Action Taken"),
    ]

    moderator = models.ForeignKey(User, on_delete=models.CASCADE)
    action_taken = models.CharField(max_length=50, choices=ACTION_CHOICES)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='moderation_logs')
    comments = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_taken} by {self.moderator} on {self.timestamp}"