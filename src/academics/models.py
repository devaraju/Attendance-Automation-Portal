from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


BRANCH_CHOICES = [('cse','CSE'),('ece','ECE'),('me','MECH'),('ce','CIVIL'),('chem','CHEM'),('mme','MME')]
YEAR_CHOICES = [('engg1','Engg-1'),('engg2','Engg-2'),('engg3','Engg-3'),('engg4','Engg-4')]

class No_of_Subjects(models.Model):
    branch = models.CharField(max_length=4, choices=BRANCH_CHOICES, default='cse')
    year = models.CharField('Batch',max_length=5, choices=YEAR_CHOICES, default='engg4')
    no_of_subjects = models.IntegerField()

    def __str__(self):
        return f'{self.no_of_subjects} subjects allowed to {self.year}{self.branch} students.'

class Subject(models.Model):
    subject_id = models.CharField(max_length=10,primary_key=True)
    subject_name = models.CharField(max_length=60, null=False)
    branch = models.CharField(max_length=4, choices=BRANCH_CHOICES, default='cse')
    year = models.CharField('Batch',max_length=5, choices=YEAR_CHOICES, default='engg4')

    def __str__(self):
        return self.subject_name+'-'+self.subject_id

class SemRegistration_201920(models.Model):
    student_id = models.OneToOneField('users.Student',on_delete=models.CASCADE)
    subjects = models.TextField()
    data_registered = models.DateTimeField('Registration DateTime',auto_now=timezone.now)

    def __str__(self):
        return f'{self.student_id} {self.subjects}'


class Teaching(models.Model):
    faculty_id = models.ForeignKey('users.Faculty',on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.faculty_id)+' - '+str(self.subject_id)
