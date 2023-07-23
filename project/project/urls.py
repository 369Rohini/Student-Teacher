"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app1 import views
from django.contrib import admin

urlpatterns = [
    # ...
    path('admin/',admin.site.urls),
    path('',views.homepage,name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('teacher/', views.teacher_page, name='teacher'),
    path('student/', views.student_page, name='student'),
    path('record_action/', views.record_action, name='record_action'),
    # path('fetch_notifications/', views.fetch_notifications, name='fetch_notifications'),
    # path('fetch_viewed_messages/', views.fetch_viewed_messages, name='fetch_viewed_messages'),
    

    # ...
]

