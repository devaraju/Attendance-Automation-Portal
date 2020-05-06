from django.urls import path

from . import views as academic_views

urlpatterns = [

    path('semregister/', academic_views.semregistration, name="sem-register"),
    
]