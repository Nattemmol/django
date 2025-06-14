from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')

    def __str__(self):
        return self.name

class Skill(models.Model):
    PRICING_MODELS = (
        ('hourly', 'Hourly'),
        ('fixed', 'Fixed'),
        ('free', 'Free'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='skills')
    media = models.FileField(upload_to='media/cvs/', null=True, blank=True)
    tags = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pricing_model = models.CharField(max_length=20, choices=PRICING_MODELS)
    availability = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.title

class SkillReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    review = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.skill} ({self.rating})"
