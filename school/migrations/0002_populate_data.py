

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import random

from django.conf import settings
from django.db import migrations, models
from django.apps import apps
from rest_framework import serializers

from school.serializers import SubjectSerializer, StudentSerializer
from school.serializers import TeacherSerializer, ClassRoomSerializer
from school.models import ClassRoom

def get_if_exists(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:  # Be explicit about exceptions
        obj = None
    return obj

def populate_initial_subject_data(apps, schema_editor):
    parameters = [{
        "name": "Math",
        "chapters": 22,
        "total_duration_min": 1800,
        "per_class_duration_min": 60,
    },{
        "name": "English",
        "chapters": 18,
        "total_duration_min": 1800,
        "per_class_duration_min": 45,
    },{
        "name": "Sports",
        "chapters": 12,
        "total_duration_min": 1800,
        "per_class_duration_min": 30,
    },{
        "name": "Health Science",
        "chapters": 18,
        "total_duration_min": 1800,
        "per_class_duration_min": 45,
    },{
        "name": "Music",
        "chapters": 15,
        "total_duration_min": 1800,
        "per_class_duration_min": 45,
    },{
        "name": "Botany",
        "chapters": 25,
        "total_duration_min": 1800,
        "per_class_duration_min": 90,
    },{
        "name": "Zoology",
        "chapters": 22,
        "total_duration_min": 1800,
        "per_class_duration_min": 90,
    },{
        "name": "Science",
        "chapters": 22,
        "total_duration_min": 1800,
        "per_class_duration_min": 90,
    },{
        "name": "Political Science",
        "chapters": 18,
        "total_duration_min": 1800,
        "per_class_duration_min": 75,
    },{
        "name": "Business Administration",
        "chapters": 20,
        "total_duration_min": 1800,
        "per_class_duration_min": 90,
    },{
        "name": "Foreign Affairs",
        "chapters": 16,
        "total_duration_min": 1800,
        "per_class_duration_min": 75,
    },{
        "name": "Negotiations",
        "chapters": 12,
        "total_duration_min": 1800,
        "per_class_duration_min": 45,
    },{
        "name": "Philosophy",
        "chapters": 18,
        "total_duration_min": 1800,
        "per_class_duration_min": 90,
    },{
        "name": "Moral Science",
        "chapters": 15,
        "total_duration_min": 1800,
        "per_class_duration_min": 45,
    }];

    Subject = apps.get_model('school', 'Subject')
    Subject.objects.all().delete()
    for param in parameters:
        serializer = SubjectSerializer(data=param)
        if serializer.is_valid():
            serializer.save()


def get_subjects_by_name(name_list):
    Subject = apps.get_model('school', 'Subject')
    subjects = []
    for name in name_list:
        subject = get_if_exists(Subject, name=name)
        if subject:
            subjects.append(subject.id)
    return subjects

def populate_initial_teacher_data(apps, schema_editor):
    parameters = [{
        "name": "Turing",
        "doj": datetime.date(2017, 8, 22),
        "salary": 1800000,
        "web_lecture": True,
        "subjects_id": get_subjects_by_name(['Math', 'English'])
    },{
        "name": "Dinho",
        "doj": datetime.date(2016, 1, 1),
        "salary": 2500000,
        "web_lecture": False,
        "subjects_id": get_subjects_by_name(['Sports', 'Health Science'])
    },{
        "name": "Adele",
        "doj": datetime.date(2015, 3, 1),
        "salary": 1000000,
        "web_lecture": False,
        "subjects_id": get_subjects_by_name(['English'])
    },{
        "name": "Freddie",
        "doj": datetime.date(2017, 8, 1),
        "salary": 2000000,
        "web_lecture": True,
        "subjects_id": get_subjects_by_name(['Music', 'English'])
    },{
        "name": "Dalton",
        "doj": datetime.date(2017, 3, 1),
        "salary": 900000,
        "web_lecture": True,
        "subjects_id": get_subjects_by_name(['Botany', 'Zoology'])
    },{
        "name": "Harish",
        "doj": datetime.date(2017, 2, 1),
        "salary": 1800000,
        "web_lecture": False,
        "subjects_id": get_subjects_by_name(['Math', 'Science'])
    },{
        "name": "Trump",
        "doj": datetime.date(2017, 8, 1),
        "salary": 800000,
        "web_lecture": False,
        "subjects_id": get_subjects_by_name(['Political Science', 'Business Administration', 'Foreign Affairs'])
    },{
        "name": "Swaraj",
        "doj": datetime.date(2019, 9, 1),
        "salary": 2800000,
        "web_lecture": True,
        "subjects_id": get_subjects_by_name(['Foreign Affairs', 'Negotiations'])
    },{
        "name": "Socrates",
        "doj": datetime.date(2015, 6, 1),
        "salary": 1150000,
        "web_lecture": True,
        "subjects_id": get_subjects_by_name(['Philosophy', 'Moral Science'])
    }];

    Teacher = apps.get_model('school', 'Teacher')
    Teacher.objects.all().delete()
    for param in parameters:
        serializer = TeacherSerializer(data=param)
        if serializer.is_valid():
            serializer.save()

def get_teachers_by_subject(subject_list):
    Teacher = apps.get_model('school', 'Teacher')
    ll = Teacher.objects.filter(
        subjects__in=subject_list
    ).distinct().values_list('id', flat=True)
    return ll

def populate_initial_classroom_data(apps, schema_editor):
    parameters = [{
        "name": "Bhabha",
        "capacity": 20,
        "web_lecture_support": True,
        "shape": ClassRoom.OVAL,
        "subjects_id": get_subjects_by_name(['Botany', 'Zoology', 'Music']),
        "teachers_id": get_teachers_by_subject(get_subjects_by_name(['Botany', 'Zoology', 'Music']))
    },{
        "name": "Kalam",
        "capacity": 40,
        "web_lecture_support": True,
        "shape": ClassRoom.RECTANGULAR,
        "subjects_id": get_subjects_by_name(['Math', 'English', 'Science']),
        "teachers_id": get_teachers_by_subject(get_subjects_by_name(['Math', 'English', 'Science']))
    },{
        "name": "Bose",
        "capacity": 20,
        "web_lecture_support": False,
        "shape": ClassRoom.CANOPY,
        "subjects_id": get_subjects_by_name(['Sports', 'Health Science']),
        "teachers_id": get_teachers_by_subject(get_subjects_by_name(['Sports', 'Health Science']))
    },{
        "name": "Raman",
        "capacity": 50,
        "web_lecture_support": True,
        "shape": ClassRoom.ELEVATED,
        "subjects_id": get_subjects_by_name(['Political Science', 'Business Administration', 'Foreign Affairs']),
        "teachers_id": get_teachers_by_subject(get_subjects_by_name(['Political Science', 'Business Administration', 'Foreign Affairs']))
    },{
        "name": "Ramanujam",
        "capacity": 20,
        "web_lecture_support": False,
        "shape": ClassRoom.OVAL,
        "subjects_id": get_subjects_by_name(['Foreign Affairs', 'Negotiations']),
        "teachers_id": get_teachers_by_subject(get_subjects_by_name(['Foreign Affairs', 'Negotiations']))
    },{
        "name": "Aryabhat",
        "capacity": 30,
        "web_lecture_support": True,
        "shape": ClassRoom.ELEVATED,
        "subjects_id": get_subjects_by_name(['Philosophy', 'Moral Science']),
        "teachers_id": get_teachers_by_subject(get_subjects_by_name(['Philosophy', 'Moral Science']))
    }];

    ClassRoom.objects.all().delete()
    for param in parameters:
        serializer = ClassRoomSerializer(data=param)
        if serializer.is_valid():
            serializer.save()

def populate_initial_student_data(apps, schema_editor):
    Student = apps.get_model('school', 'Student')
    Subject = apps.get_model('school', 'Subject')
    Teacher = apps.get_model('school', 'Teacher')
    names = ["Adam", "Alex", "Aaron", "Ben", "Carl", "Dan", "David", "Edward", "Fred", "Frank", "George", "Hal", "Hank", "Ike", "John", "Jack", "Joe", "Larry", "Monte", "Matthew", "Mark", "Nathan", "Otto", "Paul", "Peter", "Roger", "Roger", "Steve", "Thomas", "Tim", "Ty", "Victor", "Walter"]
    subjects_id = Subject.objects.all().values_list('id', flat=True)
    Student.objects.all().delete()
    for name in names:
        s = len(subjects_id) - 1
        ll = [subjects_id[random.randint(0, s)], subjects_id[random.randint(0, s)], subjects_id[random.randint(0, s)]]
        param = {
            "name": name,
            "doj": datetime.date(random.randint(2011, 2018), random.randint(1, 12), random.randint(1, 28)),
            "standard": random.randint(9, 10),
            "ranking": random.randint(0, 100),
            "subjects_id": ll,
            "teachers_id": get_teachers_by_subject(ll)
        }
        serializer = StudentSerializer(data=param)
        if serializer.is_valid():
            serializer.save()

class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_initial_subject_data, migrations.RunPython.noop),
        migrations.RunPython(populate_initial_teacher_data, migrations.RunPython.noop),
        migrations.RunPython(populate_initial_classroom_data, migrations.RunPython.noop),
        migrations.RunPython(populate_initial_student_data, migrations.RunPython.noop)
    ]