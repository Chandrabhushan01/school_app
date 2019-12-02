# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import ClassRoom
from .models import Subject
from .models import Teacher
from .models import Student
from .models import Relative

class SubjectSerializer(serializers.ModelSerializer):
    # teachers = serializers.SerializerMethodField()

    # def get_teachers(self, obj):
    #     return obj.teacher_set.all()

    class Meta(object):
        model = Subject
        fields = '__all__'

class TeacherNormalSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Teacher
        fields = '__all__'

class ClassRoomSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(read_only=True, many=True)
    subjects_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), write_only=True, many=True
    )
    teachers = TeacherNormalSerializer(read_only=True, many=True)
    teachers_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), write_only=True, many=True
    )

    class Meta(object):
        model = ClassRoom
        fields = '__all__'
    
    def create(self, validated_data):
        subjects = validated_data.pop('subjects_id')
        teachers = validated_data.pop('teachers_id')
        classroom = ClassRoom.objects.create(**validated_data)
        for sb in subjects:
            classroom.subjects.add(sb)
        for tc in teachers:
            classroom.teachers.add(tc)
        return classroom

class ClassRoomNormalSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = ClassRoom
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(read_only=True, many=True)
    subjects_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), write_only=True, many=True
    )

    class Meta(object):
        model = Teacher
        fields = '__all__'
    
    def create(self, validated_data):
        subjects = validated_data.pop('subjects_id')
        teacher = Teacher.objects.create(**validated_data)
        for sb in subjects:
            teacher.subjects.add(sb)
        return teacher

class StudentSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(read_only=True, many=True)
    subjects_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), write_only=True, many=True
    )
    teachers = TeacherSerializer(read_only=True, many=True)
    teachers_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), write_only=True, many=True
    )

    class Meta(object):
        model = Student
        fields = '__all__'
    
    def create(self, validated_data):
        subjects = validated_data.pop('subjects_id')
        teachers = validated_data.pop('teachers_id')
        student = Student.objects.create(**validated_data)
        for sb in subjects:
            student.subjects.add(sb)
        for tc in teachers:
            student.teachers.add(tc)
        return student

class StudentNormalSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Student
        fields = '__all__'

class RelativeSerializer(serializers.ModelSerializer):
    students = StudentSerializer(read_only=True, many=True)
    students_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), write_only=True, many=True
    )

    class Meta(object):
        model = Relative
        fields = '__all__'

    def create(self, validated_data):
        students = validated_data.pop('students_id')
        relative = Relative.objects.create(**validated_data)
        for st in students:
            relative.students.add(st)
        return relative