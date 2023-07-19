from django.contrib.auth.models import AbstractUser
from django.db import models


#CustomUser represents both teacher as well as student
class CustomUser(AbstractUser):
    pass

class Announcement(models.Model):
    teacher_name = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.teacher_name
