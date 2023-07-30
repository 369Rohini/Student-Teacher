from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .forms import AnnouncementForm
from .models import User, Announcement, Notification
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import User, Announcement, Notification


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

def toggle_acknowledgement(request):
    id = request.GET['notification']
    notification = Notification.objects.get(id=id)
    notification.acknowledgement = 1 if notification.acknowledgement == 0 else 0
    notification.timestamp = timezone.now()
    notification.save()
    return JsonResponse({'success': True,
                         'acknowledgement': notification.acknowledgement})


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
    announcements = Announcement.objects.filter(notification__student=user).values('message','timestamp','teacher__name','notification__id','notification__acknowledgement')
    # print(announcements)
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
    return redirect('homepage')  # Replace 'homepage' with the URL name for your homepage view


def record_action(request):
    if request.method == 'POST':
        announcement_text = request.POST.get('announcement')
        try:
            Announcement.objects.create(message=announcement_text)
            return JsonResponse({'success': True})
        except Announcement.DoesNotExist:
            pass
    return JsonResponse({'success': False})

# notifications/views.py

# from django.http import JsonResponse

# def get_announcement_details(request, announcement_id):
#     try:
#         # Fetch the details for the given announcement_id from the database (replace this with your actual logic)
#         # For example, fetch additional data from your models or other data sources based on the announcement_id
#         announcement_details = {
#             'example_key': 'example_value',
#             'another_key': 'another_value',
#             # Add other data based on your requirements
#         }
#         return JsonResponse(announcement_details)
#     except Exception as e:
#         return JsonResponse({'error': str(e)})


# def view_list(request):
#     # print(request.GET)
#     objects = notification.objects.filter(title=request.GET['acknowlwdegement'])
#     return render(request, "teacher.html", context={'objects': objects})

# from .models import Announcement

# views.py



# views.py


# views.py


@login_required
def fetch_data(request):
    # Retrieve the currently logged-in teacher user
    teacher_user = request.user
    if teacher_user.role != 'teacher':
        # Redirect or show an error message if the user is not a teacher
        return render(request, 'error.html', {'message': 'You are not authorized to view this data.'})

    # Fetch announcements where the teacher is the currently logged-in user
    announcements = Announcement.objects.filter(teacher=teacher_user)

    # Fetch notifications where the announcement is from the teacher and acknowledgement is true
    data = []
    for announcement in announcements:
        notifications = Notification.objects.filter(announcement=announcement, acknowledgement=True)
        if notifications.exists():
            # We will only consider the first notification with acknowledgement=True for each announcement
            notification = notifications.first()
            student_names = [notification.student.name for notification in notifications]
            data.append({
                'name': teacher_user.name, # Name of the logged-in teacher
                'message': announcement.message,
                'acknowledgement': notification.acknowledgement,
                'student_name': student_names,  # List of student names who acknowledged
            })

    return JsonResponse(data, safe=False)












