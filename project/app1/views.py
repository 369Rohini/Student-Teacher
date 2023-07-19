from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import Announcement

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page or a success page
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



# from django.shortcuts import render, redirect
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page or a success page
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})



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

    return render(request, 'teacher_page.html', {'form': form})


#student page....>




def student_page(request):
    announcements = Announcement.objects.all()
    return render(request, 'student_page.html', {'announcements': announcements})


def homepage(request):
    return render(request,'homepage.html')