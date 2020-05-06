from django import forms

from .models import AttendanceLog

class AttendanceLogForm(forms.ModelForm):
    class Meta:
        model = AttendanceLog
        fields = '__all__'

