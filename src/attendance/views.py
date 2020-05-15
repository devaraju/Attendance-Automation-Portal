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
import calendar
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

ALL_YEARS = AttendanceLog.objects.all().distinct('year')
ALL_SECTIONS = AttendanceLog.objects.all().distinct('section')
ALL_BRANCHES = AttendanceLog.objects.all().distinct('branch')
ALL_SUBJECTS = Subject.objects.all().distinct('subject_name')

SELECTION_DATA = {'ALL_BRANCHES':ALL_BRANCHES, 'ALL_SECTIONS':ALL_SECTIONS, 'ALL_SUBJECTS':ALL_SUBJECTS, 'ALL_YEARS':ALL_YEARS }

def get_frame(user):
    camera =cv2.VideoCapture(0)

    base_dir = os.path.dirname(os.path.realpath(__file__))
    attendance_file = os.path.join(base_dir, 'attendance_data', 'attendance_'+str(datetime.now())+'.csv')

    faculty_id = Faculty.objects.get(faculty_id=user)
    fac_teach_sub = Teaching.objects.get(faculty_id=faculty_id).subject_id
    subject_id = Subject.objects.get(subject_id=fac_teach_sub.subject_id)


    with open(attendance_file, 'w') as csv_file:
        fieldnames = ['student_id', 'date_attended', 'faculty_id','subject_id']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        all_idnos = []
        print('[INFO] Attendance Capturing...')
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
                                writer.writerow({'student_id': idno, 'date_attended': datetime.now(), 'faculty_id': faculty_id, 'subject_id':subject_id})
                                all_idnos.append(idno)

                    imgencode=cv2.imencode('.jpg', image)[1]
                    stringData=imgencode.tostring()
                    yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
            except:
                print('-> Error Occured')
    
        del(camera)
    
@login_required
def attendanceCapture(request):
    try:
        return render(request, 'attendance/attendance_capture.html', {})
    except:
        return HttpResponse('<h1>ERROR</h1>')
    

@gzip.gzip_page
def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(request.user),content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        return "error"

@login_required
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
        log = AttendanceLog.objects.all().order_by('-date_attended')
    elif user.is_staff:
        log = AttendanceLog.objects.filter(faculty_id=user).order_by('-date_attended')
    else:
        log = AttendanceLog.objects.filter(student_id=user.username).order_by('-date_attended')

    idno_query = request.GET.get('idno_extact')
    section_query = request.GET.get('section_extact')
    subject_query = request.GET.get('subject_extact')
    year_query = request.GET.get('year_extact')

    print(idno_query, section_query, subject_query, year_query)

    if idno_query != '' and idno_query is not None:
        log = log.filter(student_id=idno_query)
    if section_query != '' and section_query is not None:
        log = log.filter(section=section_query)
    if subject_query != '' and subject_query is not None:
        log = log.filter(subject_id=Subject.objects.get(subject_name=subject_query))
    if year_query != '' and year_query is not None:
        log = log.filter(year=year_query)

    context = {
        'data':log, 'user_id':user.username, 
    }
    context.update(SELECTION_DATA)
    return render(request, 'attendance/attendance_view.html', context)

@login_required
def attendanceStatistics(request):
    user = request.user
    DEAFULT_YEAR = 'engg4'
    DEAFULT_BRANCH = 'cse'
    chart_title = ''

    log_data = {}

    if not user.is_staff:
        try:
            log=AttendanceLog.objects.filter(student_id=user.username).order_by('date_attended__month')
            log_data['student'] = log_data['section'] = log_data['year'] = 1
            chart_title += str(user.username)+' '
        except:
            pass
    else:
        log=AttendanceLog.objects.all().order_by('date_attended__month')
        log_data['student'] = log.distinct('student_id').count()
        log_data['section'] = log.distinct('section').count()
        log_data['year'] = log.distinct('year').count()

    idno_query = request.GET.get('idno_extact')
    section_query = request.GET.get('section_extact')
    subject_query = request.GET.get('subject_extact')
    branch_query = request.GET.get('branch_extact')
    year_query = request.GET.get('year_extact')

    log_data['subject'] = No_of_Subjects.objects.get(year=DEAFULT_YEAR, branch=DEAFULT_BRANCH).no_of_subjects

    if idno_query != '' and idno_query is not None:
        chart_title += str(idno_query)+' '
        log = log.filter(student_id=idno_query)
        log_data['student'] = 1

    if section_query != '' and section_query is not None:
        chart_title += str(section_query)+' '
        log = log.filter(section=section_query)
        log_data['section'] = 1
    
    if subject_query != '' and subject_query is not None:
        chart_title += str(subject_query)+' '
        log = log.filter(subject_id=Subject.objects.get(subject_name=subject_query))
        log_data['subject'] = 1
    
    if year_query != '' and year_query is not None:
        chart_title += str(year_query)+' '
        log = log.filter(year=year_query)
        log_data['year'] = 1

    log_months = log.distinct('date_attended__month')
    working_days = {}
    attended_days = {}

    for log_month in log_months:
        dt = log_month.date_attended
        month_name = calendar.month_name[dt.month]
        _, working_days[month_name] = calendar.monthrange(dt.year, dt.month)
        temp_attended_days = log.filter(date_attended__month=dt.month).count()
        
        for key,value in log_data.items():
            temp_attended_days /= value 
        attended_days[month_name] = temp_attended_days

    if chart_title is '':
        chart_title = DEAFULT_YEAR +' '+ DEAFULT_BRANCH

    context = { 'chart_title':chart_title.upper(), 'months':list(working_days.keys()), 'no_of_working_days':list(working_days.values()), 'no_of_attended_days':list(attended_days.values())}
    context.update(SELECTION_DATA)
    

    return render(request, 'attendance/attendance_statistics.html', context)
