# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=64, unique=True, null=True, blank=True)
    chapters = models.IntegerField(default=0)
    total_duration_min = models.IntegerField(default=0)
    per_class_duration_min = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Teacher(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    doj = models.DateField(null=True, blank=True)
    salary = models.FloatField(default=0)
    web_lecture = models.BooleanField(default=False)
    subjects = models.ManyToManyField(Subject)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class ClassRoom(models.Model):
    OVAL = 'oval'
    RECTANGULAR = 'rectangular'
    CANOPY = 'canopy'
    ELEVATED = 'elevated'
    SHAPE_OPTION = (
        (OVAL, 'oval'),
        (RECTANGULAR, 'rectangular'),
        (CANOPY, 'canopy'),
        (ELEVATED, 'elevated')
    )
    name = models.CharField(max_length=64, unique=True, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    web_lecture_support = models.BooleanField(default=False)
    shape = models.CharField(
        max_length=64, choices=SHAPE_OPTION, default=None, null=True, blank=True
    )
    subjects = models.ManyToManyField(Subject)
    teachers = models.ManyToManyField(Teacher)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Student(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    doj = models.DateField(null=True, blank=True)
    standard = models.IntegerField(null=True, blank=True)
    roll_no = models.AutoField(primary_key=True)
    ranking = models.IntegerField(null=True, blank=True)
    subjects = models.ManyToManyField(Subject)
    teachers = models.ManyToManyField(Teacher)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Relative(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    relation = models.CharField(max_length=64, null=True, blank=True)
    students = models.ManyToManyField(Student)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)