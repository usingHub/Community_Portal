from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# -------------------------
# Custom User Model
# -------------------------
class CustomUser(AbstractUser):
    USER_ROLES = (
        ('requester', 'Requester'),
        ('donor', 'Donor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='requester')
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# -------------------------
# Category Model
# -------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# -------------------------
# Request Model
# -------------------------
class Request(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.status})"


# -------------------------
# Offer Model
# -------------------------
class Offer(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.status})"
