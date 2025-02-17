from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Profile(AbstractUser):
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

from django.contrib.auth.models import User
from django.db import models

class Tasks(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
    ]
    
    task_id = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    reference = models.FileField(upload_to='video_courses/', blank=True, null=True)
    price = models.CharField(max_length=250, blank=True)
    deadline = models.CharField(max_length=100, blank=True)
    topic = models.CharField(max_length=50, blank=True)
    level = models.CharField(max_length=50, blank=True)
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    accepted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.task_id


# class UserProgress(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         related_name='user_progress',
#         on_delete=models.CASCADE,
#     )
#     course = models.ForeignKey(Video_courses, on_delete=models.CASCADE)
#     topic = models.ForeignKey(Video_courses, on_delete=models.CASCADE, related_name='topic_progress')
#     progress = models.PositiveIntegerField(default=0)
#     hours_watched = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)



class SubscriptionModule(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., Basic, Advanced, Hybrid
    price = models.DecimalField(max_digits=10, decimal_places=1)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    purchased_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='purchased_transactions',
        on_delete=models.CASCADE,
        db_index=True,
        default=1
    )
    item = models.ForeignKey(SubscriptionModule, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.item}"

class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(SubscriptionModule, related_name='subscriptions', on_delete=models.CASCADE,default=None)
    transaction = models.ForeignKey(Transaction, related_name='subscriptions', on_delete=models.CASCADE,default=None)
    

    def __str__(self):
        return f"{self.user} subscribed to {self.module}"
