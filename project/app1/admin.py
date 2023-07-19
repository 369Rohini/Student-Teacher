from django.contrib import admin
from .models import Announcement,CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Announcement)