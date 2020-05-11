from django.contrib import admin

from .models import *

class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ['id','student_id', 'faculty_id', 'subject_id', 'date_attended']
    list_filter = ['date_attended', 'subject_id']

admin.site.register(AttendanceLog, AttendanceLogAdmin)