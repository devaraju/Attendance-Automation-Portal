from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group

from .models import Student, Faculty
from .forms import StudentRegisterForm, FacultyRegisterForm, StudentUpdateForm, FacultyUpdateForm

def studentRegister(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save();
            messages.success(request, f'Account has been created! You are now able to login')
            return redirect('login')
    else:
        form = StudentRegisterForm()
    return render(request, 'users/register.html',{ 'form':form, 'user_type':'Student' })

def facultyRegister(request):
    if request.method == 'POST':
        form = FacultyRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save();
            messages.success(request, f'Account has been created! You are now able to login')
            return redirect('login')
    else:
        form = FacultyRegisterForm()
    return render(request, 'users/register.html',{ 'form':form , 'user_type':'Faculty' })

# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = FacultyUpdateForm(request.POST, instance=request.user.faculty) if user.is_staff else StudentUpdateForm(request.POST, instance=request.user.student)
#         # if user.is_staff:
#         #     form = FacultyUpdateForm(request.POST, instance=request.user.faculty)
#         # else:
#         #     form = StudentUpdateForm(request.POST, instance=request.user.student)

#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Profile has been updated!')
#             return redirect('profile')
#     else:
#         form = FacultyUpdateForm(instance=request.user.faculty) if user.is_staff else StudentUpdateForm(instance=request.user.student)
#         # if user.is_staff:
#         #     form = FacultyUpdateForm(instance=request.user.faculty)
#         # else:
#         #     form = StudentUpdateForm(instance=request.user.student)
#     context = {'form': form}
#     return render(request, 'users/profile.html', context)
