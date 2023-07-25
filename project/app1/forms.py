from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Announcement, Notification


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    name = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['message']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AnnouncementForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        announcement = super().save(commit=False)
        announcement.teacher = self.request.user
        if commit:
            announcement.save()
            students = User.objects.filter(role='student')
            for student in students:
                notification = Notification(student=student, announcement=announcement)
                notification.save()
        return announcement
