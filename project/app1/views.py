from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import AnnouncementForm
from .models import User, Announcement, Notification
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def signup_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
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
        user = User.objects.create_user(username=username, name=name, password=password1, role=role)
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')

    return render(request, 'signup.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'student':
                return redirect('student')  # Redirect to the student page
            elif user.role == 'teacher':
                return redirect('teacher')  # Redirect to the teacher page

            # return redirect('dashboard')  # If the role is not defined or not 'student' or 'teacher', redirect to a generic dashboard page
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

@login_required
def student_page(request):
    user = request.user
    if not hasattr(user, 'role') or user.role != 'student':
        raise PermissionError('Permission denied')
    announcements = Announcement.objects.filter(notification__student=user)
    return render(request, 'student.html', {'announcements': announcements})

@login_required
def teacher_page(request):
    user = request.user
    if not hasattr(user, 'role') or user.role != 'teacher':
        raise PermissionError('Permission denied')
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return render(request, 'teacher_success.html')  # Render a success page or redirect as needed
    else:
        form = AnnouncementForm(request=request)

    return render(request, 'teacher.html', {'form': form})


def homepage(request):
    return render(request, 'homepage.html')

def logout_view(request):
    logout(request)
    return redirect('homepage') 


def record_action(request):
    if request.method == 'POST':
        announcement_text = request.POST.get('announcement')
        try:
            Announcement.objects.create(message=announcement_text)
            return JsonResponse({'success': True})
        except Announcement.DoesNotExist:
            pass
    return JsonResponse({'success': False})


def fetch_notifications(request):
    notifications = Notification.objects.all()
    data = []
    for notification in notifications:
        data.append({
            'teacher_name': notification.teacher.name,
            'message': notification.message,
            'student_username': notification.student.username
        })
    return JsonResponse(data, safe=False)


def fetch_viewed_messages(request):
    if request.method == 'GET':
        notifications = Notification.objects.all()

        viewed_messages = []
        for notification in notifications:
            viewed_messages.append(f"{notification.student_username}: {notification.message}")

        return JsonResponse(viewed_messages, safe=False)
