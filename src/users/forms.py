from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Student, Faculty

class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for key, field in self.fields.items():
    #         field.widget.attrs.update({'placeholder': field.label})

class FacultyRegisterForm(UserCreationForm):
    is_staff = forms.BooleanField(initial=True, widget=forms.HiddenInput)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update({'placeholder': field.label})

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'student_id']

class FacultyUpdateForm(ModelForm):
    class Meta:
        model = Faculty
        exclude = ['user', 'faculty_id']
