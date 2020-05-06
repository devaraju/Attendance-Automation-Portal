from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import datetime

class AttendanceLog(models.Model):
    student_id = models.CharField(max_length=7, null=False)
    faculty_id = models.ForeignKey('users.Faculty', on_delete=models.DO_NOTHING)
    subject_id = models.ForeignKey('academics.Subject', on_delete=models.DO_NOTHING)
    date_attended = models.DateTimeField('Date & Time', auto_now_add=True)

    class Meta:
        unique_together = (("student_id","faculty_id","date_attended","subject_id"))

    def __str__(self):
        return f'{self.student_id} - {self.date_attended} - {self.subject_id} - {self.faculty_id}'
