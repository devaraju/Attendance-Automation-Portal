from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import datetime

BRANCH_CHOICES = [('cse','CSE'),('ece','ECE'),('me','MECH'),('ce','CIVIL'),('chem','CHEM'),('mme','MME')]
YEAR_CHOICES = [('engg1','Engg-1'),('engg2','Engg-2'),('engg3','Engg-3'),('engg4','Engg-4')]
SECTION_CHOICES = [('sec1','SEC-1'),('sec2','SEC-2'),('sec3','SEC-3'),('sec4','SEC-4')]

class AttendanceLog(models.Model):
    student_id = models.CharField(max_length=7, null=False)
    faculty_id = models.ForeignKey('users.Faculty', on_delete=models.DO_NOTHING)
    subject_id = models.ForeignKey('academics.Subject', on_delete=models.DO_NOTHING)
    date_attended = models.DateTimeField('Date & Time')
    branch = models.CharField(max_length=8, choices=BRANCH_CHOICES, default='cse')
    section = models.CharField(max_length=8, choices=SECTION_CHOICES, default='sec2')
    year = models.CharField('Batch',max_length=8, choices=YEAR_CHOICES, default='engg4')

    class Meta:
        unique_together = (("student_id","faculty_id","date_attended","subject_id"))

    def __str__(self):
        return f'{self.student_id} - {self.date_attended} - {self.subject_id} - {self.faculty_id}'
