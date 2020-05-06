from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone

from django.views.decorators import gzip
from datetime import datetime
import face_recognition
import json
import time
import cv2
import sys
import csv
import os

from users.models import Student, Faculty
from attendance.models import AttendanceLog
from academics.models import No_of_Subjects, Subject, SemRegistration_201920, Teaching
from .forms import AttendanceLogForm

from .facial_mathcing.testing import getFacialMatching

# <<< USER DEFINED VIEWS >>>

def get_frame():
    camera =cv2.VideoCapture(-1)

    base_dir = os.path.dirname(os.path.realpath(__file__))
    attendance_file = os.path.join(base_dir, 'attendance_data', 'attendance_'+str(datetime.now())+'.csv')

    with open(attendance_file, 'w') as csv_file:
        fieldnames = ['student_id', 'date_attended', 'faculty_id','subject_id']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        all_idnos = []
        while True:
            try:
                ret, image = camera.read()
                if ret:
                    image = cv2.flip(image, 1)
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    faces = face_recognition.face_locations(rgb_image, model="hog")
                    if len(faces) != 0:
                        for (top, right, bottom, left) in faces:
                            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                        
                        idnos = getFacialMatching(rgb_image, faces)
                        for idno in idnos:
                            if idno not in all_idnos:
                                writer.writerow({'student_id': idno, 'date_attended': datetime.now(), 'faculty_id': 'testing', 'subject_id':'test-sub'})
                                all_idnos.append(idno)

                    imgencode=cv2.imencode('.jpg', image)[1]
                    stringData=imgencode.tostring()
                    yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
            except:
                print('-> Error Occured')
    
        del(camera)
    
    
def attendanceCapture(request):
    try:
        return render(request, 'attendance/attendance_capture.html', {})
    except:
        return HttpResponse('<h1>ERROR</h1>')
    

@gzip.gzip_page
def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        return "error"


def attendanceUpload(request):
    data = []
    file_name = 'attendance_sample.csv'
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            data.append(dict(row))
    
    if request.method == 'POST':
        for i in range(1,len(data)+1):
            if request.POST.get('check_'+str(i), 'off') == 'on':
                student_id = request.POST['student_id_'+str(i)]
                faculty_id = request.POST['faculty_id_'+str(i)]
                subject_name = request.POST['subject_id_'+str(i)]
                date_attended = request.POST['date_attended_'+str(i)]
                
                # print(student_id, subject_name, date_attended)
                dt=[int(i) for i in date_attended.split(',')]
                log = AttendanceLog.objects.create(student_id=student_id,faculty_id=Faculty.objects.get(faculty_id=faculty_id),subject_id=Subject.objects.get(subject_name=subject_name), date_attended=datetime(*dt))

        messages.success(request, f'Log uploaded successful.')
        return redirect('home')

    else:
        return render(request, 'attendance/attendance_upload.html', {'data':data, 'file_name':file_name})

@login_required
def attendanceView(request):
    user = request.user
    if user.is_superuser:
        qs = AttendanceLog.objects.all().order_by('-date_attended')

    elif user.is_staff:
        qs = AttendanceLog.objects.filter(faculty_id=user).order_by('-date_attended')
        idno_contains_query = request.GET.get('idno_contains')
        if idno_contains_query != '' and idno_contains_query is not None:
            qs = qs.filter(student_id__icontains=idno_contains_query)

    else:
        qs = AttendanceLog.objects.filter(student_id=user.username).order_by('-date_attended')

    return render(request, 'attendance/attendance_view.html', {'data':qs, 'user_id':user.username})

@login_required
def attendanceStatistics(request):
    user = request.user
    sem_1_months = [8,9,10,11]
    sem_2_months = [12,1,2,3,4]

    x_labels = ['JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


    if user.is_staff or user.is_superuser:
        qs = AttendanceLog.objects.all()
        idno_contains_query = request.GET.get('idno_contains')
        if idno_contains_query != '' and idno_contains_query is not None:
            qs = qs.filter(student_id__icontains=idno_contains_query)

    else:
        qs = AttendanceLog.objects.filter(student_id=user.username).order_by('-date_attended')
    context = {'data':qs, 'user_id':user.username, 'x_labels':x_labels}
    return render(request, 'attendance/attendance_statistics.html', context)




# ======================================================================
# def attendanceView(request):
#     user = request.user
#     # subjects = getRegSubjects(user)
#     attendance_data = []
#     if request.method == 'POST' and request.POST["subject"] != 'all':
#         subject_name = request.POST["subject"] 
#         # attendance_data = getSubjectAttendance(user, subject_name)
#         attendance_data = getDummySubjectAttendance(user, subject_name)
#     else:
#         # attendance_data = getUserAttendance(user)
#         attendance_data = getDummyUserAttendance(user)
    
#     paginator = Paginator(attendance_data, 8)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     context = {'data':attendance_data, "subjects":subjects, "page_obj":page_obj}
#     return render(request, 'attendance/attendance_list.html', context)  
#     return render(request, 'attendance/attendance_view.html', {})


# from .attendance_automation.sample import *

# @login_required
# def attendance_upload(request):
#     data = getDummyUploadData()[:6]
    
#     if request.method == 'POST':
#         for i in range(len(data)):
#             if request.POST.get(str(i), 'off') != 'off':
#                 student_id = request.POST['student_id_'+str(i)]
#                 faculty_name = request.POST['faculty_id_'+str(i)]
#                 subject_name = request.POST['subject_id_'+str(i)]
#                 date_attended = request.POST['date_attended_'+str(i)]
                
#                 log = AttendanceLog(student_id=student_id,faculty_id=Faculty.objects.get(faculty_name=faculty_name),subject_id=Subject.objects.get(subject_name=subject_name), date_attended=date_attended)
#                 log.save()

#         messages.success(request, f'Log uploaded successful.')
#         return redirect('attendance-list')

    
#     context = { "data":data}
#     return render(request, 'attendance/attendance_upload.html', context)

# def sample(request):
#     data = getDummyUploadData()[:5]

#     if request.method == 'POST':
#         print("attends")

#         for i in range(len(data)):
#             print(request.POST.get(str(i),'off'))

    
#     return render(request, 'attendance/sample.html', {"data":data,"indexes":[]})



# @login_required
# def attendance_list(request):
#     user = request.user
#     subjects = getRegSubjects(user)
#     attendance_data = []
#     if request.method == 'POST' and request.POST["subject"] != 'all':
#         subject_name = request.POST["subject"] 
#         # attendance_data = getSubjectAttendance(user, subject_name)
#         attendance_data = getDummySubjectAttendance(user, subject_name)
#     else:
#         # attendance_data = getUserAttendance(user)
#         attendance_data = getDummyUserAttendance(user)
    
#     paginator = Paginator(attendance_data, 8)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     context = {'data':attendance_data, "subjects":subjects, "page_obj":page_obj}
#     return render(request, 'attendance/attendance_list.html', context)        


# def getSubjectAttendance(userid,subject_name):
#     data = []
#     sno = 1
#     subject_id = Subject.objects.get(subject_name=subject_name).subject_id
#     queryset = AttendanceLog.objects.filter(student_id=userid.username, subject_id=subject_id).order_by('-date_attended')
#     for query in queryset:
#         data.append([sno, userid, subject_name,  query.faculty_id,  query.date_attended])
#         sno +=1
#     return data

# def getUserAttendance(userid):
#     data = []
#     sno = 1
#     try:
#         queryset = AttendanceLog.objects.filter(student_id=Student.objects.get(student_id=userid)).order_by('-date_attended')
#         for query in queryset:
#             data.append([sno,userid, query.subject_id, query.faculty_id, query.date_attended])
#             sno += 1
#     except:
#         pass
#     return data

# def getRegSubjects(userid):
#     subjects = []
#     try:
#         queryset = SemRegistration_201920.objects.get(student_id=Student.objects.get(student_id=userid.username)).subjects
#         subjects = queryset.split('+')
#     except:
#         pass
#     return subjects

# #-----------------------------DUMMY DATA------------------------------

# def getDummyUserAttendance(userid):
#     parent_path = os.path.dirname(os.path.abspath(__file__))
#     file_path = parent_path+"/attendance_data.json"
#     with open(file_path) as fp:
#         all_data = json.load(fp)
#     data = []
#     sno = 1
#     for row in all_data:
#         if(row["student_id"]==userid.username):
#             data.append([sno, row["student_id"], row["subject_id"], row["faculty_id"], row["date_attended"]])
#             sno +=1
#     return data

# def getDummySubjectAttendance(userid, subject_name):
#     parent_path = os.path.dirname(os.path.abspath(__file__))
#     file_path = parent_path+"/attendance_data.json"
#     with open(file_path) as fp:
#         all_data = json.load(fp)
#     data = []
#     sno = 1

#     for row in all_data:
#         if(row["student_id"]==userid.username and row["subject_id"]==subject_name):
#             data.append([sno, row["student_id"], row["subject_id"], row["faculty_id"], row["date_attended"]])
#             sno +=1
#     return data

# def getDummyUploadData():
#     parent_path = os.path.dirname(os.path.abspath(__file__))
#     file_path = parent_path+"/attendance_data.json"
#     with open(file_path, encoding='utf-8') as fp:
#         all_data = json.loads(fp.read())

#     # with open('movie_data.json', encoding='utf-8') as data_file:
#     # json_data = json.loads(data_file.read())
    
#     # data = []
#     # n=1
#     # for row in all_data:
#     #     n += 1
#     #     data.append([row["student_id"], row["subject_id"], row["faculty_id"], row["date_attended"]])
#     #     if(n==2):
#     #         break
#     # return data
#     return all_data

# def getDummySubjectUploadData(subject_name):
#     parent_path = os.path.dirname(os.path.abspath(__file__))
#     file_path = parent_path+"/attendance_data.json"
#     with open(file_path) as fp:
#         all_data = json.load(fp)
#     data = []
#     for row in all_data:
#         if row["subject_id"]==subject_name:
#             data.append([row["student_id"], subject_name, row["faculty_id"], row["date_attended"]])
#     return data

# def getDummyStudentSubjectUploadData(student_id,subject_name):
#     parent_path = os.path.dirname(os.path.abspath(__file__))
#     file_path = parent_path+"/attendance_data.json"
#     with open(file_path) as fp:
#         all_data = json.load(fp)
#     data = []
#     for row in all_data:
#         if row["subject_id"]==subject_name and row["student_id"]==student_id:
#             data.append([student_id, subject_name, row["faculty_id"], row["date_attended"]])
#     return data

# def getAllSubjects(year,branch):
#     subjects = []
#     queryset = Subject.objects.filter(year=year,branch=branch)
#     for query in queryset:
#         subjects.append(query.subject_name)
#     return subjects