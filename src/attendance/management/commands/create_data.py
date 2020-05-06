from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from users.models import Faculty
from attendance.models import AttendanceLog
from academics.models import Subject

import os
import json
from datetime import datetime

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('attendance_file', type=str,
    #                         help="JSON file that contains attendance data")
    #     parser.add_argument('subjects_file', type=str,
    #                         help="JSON file that contains subjects data")

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        # attendance_file = kwargs["sample_attendance_data.json"]
        # subjects_file = kwargs["subjects_data.json"]
        attendance_file = os.path.join(base_dir, 'sample_attendance_data.json')
        subjects_file = os.path.join(base_dir, 'subjects_data.json')
        # print(attendance_file, subjects_file)
        
        # >>> SUBJECTS DATA <<<
        with open(f"{subjects_file}") as file:
            data = json.load(file)

            for row in data:
                subject_id = row["subject_id"]
                subject_name = row["subject_name"]
                branch = row["branch"]
                year = row["year"]

                subject = Subject.objects.get_or_create(
                    subject_id=subject_id,
                    subject_name=subject_name,
                    branch=branch,
                    year=year
                )

        # >>> ATTENDANCE DATA <<<
        with open(f"{attendance_file}") as file:
            data = json.load(file)

            for row in data:
                student_id = row["student_id"]
                faculty_id = row["faculty_id"]
                subject_id = row["subject_id"]
                date_attended = row["date_attended"]

                try:
                    faculty = Faculty.objects.get(faculty_id = faculty_id)
                except:
                    user=User.objects.create_user(username=faculty_id, password='fac_123',is_staff=True)
                    faculty = Faculty.objects.get(faculty_id = faculty_id)
                    self.stdout.write(self.style.SUCCESS(f'successfully added {faculty_id}'))

                try:
                    dt=[int(i) for i in date_attended.split(',')]
                    log = AttendanceLog.objects.create(student_id=student_id,faculty_id=Faculty.objects.get(faculty_id=faculty_id),subject_id=Subject.objects.get(subject_name=subject_id), date_attended=datetime(*dt))
                except:
                    self.stdout.write(self.style.ERROR(f'Error occured with {student_id}-{date_attended}-{subject_id}'))

        self.stdout.write(self.style.SUCCESS('successfully added attendance data.'))

    

