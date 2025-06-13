from django.db import models

class NGOPartner(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='media/logos/')
    link = models.URLField()

    def __str__(self):
        return self.name


class BusinessAd(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    business_name = models.CharField(max_length=100)
    media = models.ImageField(upload_to='media/ads/')
    valid_until = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.business_name}"
