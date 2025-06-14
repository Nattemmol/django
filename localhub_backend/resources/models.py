from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    description = models.TextField()
    condition = models.CharField(max_length=100)
    rental_terms = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    condition_report = models.FileField(upload_to='media/reports/', null=True, blank=True)
    material = models.FileField(upload_to='media/material/', null=True, blank=True)
    video = models.URLField(blank=True, null=True)



    def __str__(self):
        return self.title

class Rental(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
        ('damaged', 'Damaged'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    agreement_signed = models.BooleanField(default=False)

class ResourceReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
