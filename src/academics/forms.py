from django.forms import ModelForm

from .models import SemRegistration_201920 

class SemRegistrationForm(ModelForm):

    class Meta:
        model = SemRegistration_201920
        fields = ['subjects']
