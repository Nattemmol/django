from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# User Model
class User(AbstractBaseUser):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

# Category Model
class Category(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    icon_name = models.CharField(max_length=50)  # Store icon name as a string

    def __str__(self):
        return self.name

# Guest Model
class Guest(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    image_path = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Event Model
class Event(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    image_path = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    duration = models.CharField(max_length=50)
    punch_line1 = models.CharField(max_length=255, null=True, blank=True)
    punch_line2 = models.CharField(max_length=255, null=True, blank=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_events')
    categories = models.ManyToManyField(Category, related_name='events')
    gallery_images = models.JSONField(default=list)  # Store a list of image paths
    guests = models.ManyToManyField(Guest, related_name='events')  # Many-to-Many with Guest

    def __str__(self):
        return self.title
