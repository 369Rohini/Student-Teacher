from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    name = models.CharField(max_length=100, default='Default Name')
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.name


class Announcement(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.teacher}: {self.message}"


class Notification(models.Model):
    student = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    announcement = models.ForeignKey(Announcement, on_delete=models.PROTECT, default=None)
    acknowledgement = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=None, null=True)
