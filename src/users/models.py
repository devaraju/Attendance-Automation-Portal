from django.db import models
from django.contrib.auth.forms import User

GENDER_CHOICES = [('m','MALE'),('f','FEMALE')]
BRANCH_CHOICES = [('cse','CSE'),('ece','ECE'),('me','MECH'),('ce','CIVIL'),('chem','CHEM'),('mme','MME')]
YEAR_CHOICES = [('engg1','Engg-1'),('engg2','Engg-2'),('engg3','Engg-3'),('engg4','Engg-4')]
SECTION_CHOICES = [('sec1','SEC-1'),('sec2','SEC-2'),('sec3','SEC-3'),('sec4','SEC-4')]

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=7, unique=True)
    fullname = models.CharField(max_length=50)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES, default='m')
    branch = models.CharField(max_length=4, choices=BRANCH_CHOICES, default='cse')
    section = models.CharField(max_length=5, choices=SECTION_CHOICES, default='sec2')
    year = models.CharField('Batch',max_length=5, choices=YEAR_CHOICES, default='engg4')

    def __str__(self):
        return f'{self.student_id} - {self.branch} - {self.year}'

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=30, unique=True)
    faculty_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES, default='m')
    
    def __str__(self):
        return f'{self.faculty_id} - {self.faculty_name}'

