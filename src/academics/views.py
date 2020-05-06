from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group

from .forms import *
from .models import *
from users.models import Student

@login_required
def semregistration(request):
    user = request.user
    reg_status = isRegistered(user)
    if reg_status:
        reg_data = getRegistedDetails(user)
        return render(request, 'academics/semregister.html',{'reg_data':reg_data, 'reg_status':reg_status })
        
    else:
        student = Student.objects.get(student_id=user.username)
        subjects_avail = getAllSubjects(student)
        subjects_count = getSubjectsCount(student)

        if request.method == 'POST':
            subjects = [ request.POST['subject'+str(x)] for x in subjects_count]
            subjects = '+'.join(subjects)
            reg = SemRegistration_201920.objects.create(student_id=Student.objects.get(student_id=request.user.username), subjects=subjects)
            messages.success(request, f'Registration success')
            return redirect('sem-register')
        else:
            context = {'subjects_avail':subjects_avail, 'subjects_count':subjects_count,'isRegistered':isRegistered }
            return render(request, 'academics/semregister.html', context)


def getRegistedDetails(user):
    reg_subjects = SemRegistration_201920.objects.get(student_id=Student.objects.get(student_id=user.username)).subjects
    reg_data= reg_subjects.split('+')
    
    return reg_data

def isRegistered(user):
    try:
        print(user, user.username)
        user_reg_data = SemRegistration_201920.objects.get(student_id=Student.objects.get(student_id=user.username))
        print("================")
        return True
    except:
        return False

def getSubjectsCount(student):
    no_of_subjects = No_of_Subjects.objects.get(year=student.year, branch=student.branch).no_of_subjects
    subjects_count = [ x for x in range(1, no_of_subjects+1)]
    return subjects_count

def getAllSubjects(student):
    all_subjects = []
    queryset = Subject.objects.filter(year=student.year, branch=student.branch)
    for query in queryset:
        all_subjects.append(query.subject_name)
    return all_subjects