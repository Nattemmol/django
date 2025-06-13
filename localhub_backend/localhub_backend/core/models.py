from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g. Admin, Moderator, etc.

    def __str__(self):
        return self.name

class Location(models.Model):
    lat = models.FloatField()
    long = models.FloatField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=False)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="media/profiles/", blank=True, null=True)
    languages = models.JSONField(blank=True, null=True)  # list of strings
    badges = models.JSONField(blank=True, null=True)     # list of badges
    skills_offered = models.JSONField(blank=True, null=True)
    skills_requested = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification')
    badge_type = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    date_verified = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Verified: {self.is_verified}"
