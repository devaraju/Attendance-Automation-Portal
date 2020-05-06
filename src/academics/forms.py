from django.forms import ModelForm

from .models import *

class SemRegistrationForm(ModelForm):
    
    class Meta:
        model = SemRegistration_201920
        fields = ['subjects']