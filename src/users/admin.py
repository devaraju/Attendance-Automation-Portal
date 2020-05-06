from django.contrib import admin

from .models import Student, Faculty

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id','fullname','branch','section','year')
    list_filter = ['year', 'branch']

admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty)

