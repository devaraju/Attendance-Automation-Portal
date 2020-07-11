from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from users.models import Faculty
from attendance.models import AttendanceLog
from academics.models import Subject, No_of_Subjects

import os
import json
import pytz
from datetime import datetime

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('attendance_file', type=str, help="JSON file that contains attendance data")
    #     parser.add_argument('subjects_file', type=str, help="JSON file that contains subjects data")

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        # attendance_file = kwargs["sample_attendance_data.json"]
        # subjects_file = kwargs["subjects_data.json"]
        attendance_file = os.path.join(base_dir, 'sample_attendance_data.json')
        subjects_file = os.path.join(base_dir, 'subjects_data.json')

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
        STUDENT_IDS = []
        FACULTY_IDS = []
        SUBJECT_IDS = []
        REG_SUBJECTS = {}
        FACULTY_SUBJECT = {}

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

                if student_id not in STUDENT_IDS:
                    STUDENT_IDS.append(student_id)
                    REG_SUBJECTS[student_id] = []

                if subject_id not in REG_SUBJECTS[student_id]:
                    REG_SUBJECTS[student_id].append(subject_id)
                if subject_id not in FACULTY_SUBJECT:
                    FACULTY_SUBJECT[subject_id] = faculty_id


        YEAR = 2020
        MONTHS = [1,2,3,4,5]
        class_hours = [9,10,11]

        PONGAL_START = datetime(2020,1,11, tzinfo=pytz.timezone("Asia/Kolkata"))
        PONGAL_END = datetime(2020,1,18, tzinfo=pytz.timezone("Asia/Kolkata"))
        SEMESTER_END = datetime(2020,5,6, tzinfo=pytz.timezone("Asia/Kolkata"))

        for month in MONTHS:
            for date in range(1,32):
                try:
                    curr_datetime = datetime(YEAR, month, date, 0, 25, tzinfo=pytz.timezone("Asia/Kolkata"))
                    if curr_datetime.weekday() == 6 or curr_datetime > SEMESTER_END:
                        continue
                    if curr_datetime >= PONGAL_START and curr_datetime <= PONGAL_END:
                        continue
                except:
                    self.stdout.write(self.style.ERROR(f'Error occured with {curr_datetime}'))
                    continue

                for student_id in STUDENT_IDS:
                    for reg_subject, class_hour in zip(REG_SUBJECTS[student_id],class_hours):
                        try:
                            curr_datetime = curr_datetime.replace(hour=class_hour)
                            log = AttendanceLog.objects.get_or_create(student_id=student_id,faculty_id=Faculty.objects.get(faculty_id=FACULTY_SUBJECT[reg_subject]),subject_id=Subject.objects.get(subject_name=reg_subject), date_attended=curr_datetime)
                        except:
                            self.stdout.write(self.style.ERROR(f'Error occured with {student_id}-{date_attended}-{subject_id}'))
        subs_cnt = No_of_Subjects.objects.get_or_create(no_of_subjects=3)
        self.stdout.write(self.style.SUCCESS('successfully added attendance data.'))
