# app_name/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from app1.models import User  # Replace 'app_name' with the actual name of your app

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        # email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup')

        # Create a new user
        user = User.objects.create_user(username=username, password=password1, role=role)
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login(request)

            if user.role == 'student':
                return redirect('student_page.html')  # Redirect to the student page
            elif user.role == 'teacher':
                return redirect('teacher_page.html')  # Redirect to the teacher page

            # return redirect('dashboard')  # If the role is not defined or not 'student' or 'teacher', redirect to a generic dashboard page
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


def student_page(request):
    return render(request, 'student.html')

    # Add any other additional fields related to the user here (e.g., profile picture, date of birth, etc.)


def homepage(request):
    return render(request, 'homepage.html')

#announcement......>

from .forms import AnnouncementForm

def teacher_page(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'teacher_success.html')  # Render a success page or redirect as needed
    else:
        form = AnnouncementForm()

    return render(request, 'teacher.html', {'form': form})


#student page....>




def student(request):
    announcements = Announcement.objects.all()
    
    return render(request, 'student.html', {'announcements': announcements})



# def homepage(request):
#     return render(request,'homepage.html')


from django.http import JsonResponse
from .models import Announcement

def record_action(request):
    if request.method == 'POST':
        announcement_text = request.POST.get('announcement')
        student_username = request.POST.get('username')
        try:
            announcement = Announcement.objects.get(message=announcement_text)
            # Notification.objects.create(teacher_name=announcement.teacher_name, message=announcement.message, student_username=student_username)
            return JsonResponse({'success': True})
        except Announcement.DoesNotExist:
            pass
    return JsonResponse({'success': False})

def fetch_notifications(request):
    notifications = Notification.objects.all()
    data = []
    for notification in notifications:
        data.append({
            'teacher_name': notification.teacher_name,
            'message': notification.message,
            'student_username': notification.student_username
        })
    return JsonResponse(data, safe=False)

# Other views ...

def fetch_viewed_messages(request):
    if request.method == 'GET':
        # Fetch notifications associated with liked messages
        notifications = Notification.objects.all()

        # Create a list to store the viewed messages with the associated student name
        viewed_messages = []
        for notification in notifications:
            viewed_messages.append(f"{notification.student_username}: {notification.message}")

        return JsonResponse(viewed_messages, safe=False)
