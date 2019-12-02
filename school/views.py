import datetime
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Count, Sum, F

from rest_framework import viewsets
from rest_framework import status

from .models import Subject, Student, ClassRoom, Teacher, Relative
from .serializers import SubjectSerializer, ClassRoomSerializer
from .serializers import TeacherSerializer, StudentSerializer
from .serializers import StudentNormalSerializer, ClassRoomNormalSerializer

# Create your views here.

class IndexView(View):
    template_name = 'school/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

class ClassRoomView(View):
    template_name = 'school/tabular_preview.html'

    def get(self, request, *args, **kwargs):
        classrooms = ClassRoom.objects.all().prefetch_related('subjects', 'teachers')
        serilizer = ClassRoomSerializer(classrooms, many=True)
        classrooms_list = []
        for cr in serilizer.data:
            subjects = set()
            teachers = set()
            for sub in cr['subjects']:
                subjects.add(sub['name'])
            for tch in cr['teachers']:
                teachers.add(tch['name'])
            obj = {
                'name': cr['name'],
                'shape': cr['shape'],
                'capacity': cr['capacity'],
                'web_lecture_support': cr['web_lecture_support'],
                'subjects': list(subjects),
                'teachers': list(teachers)
            }
            classrooms_list.append(obj)
        context = {
            'classrooms': classrooms_list
        }
        return render(request, self.template_name, context)

class TeacherSearchView(View):
    template_name = 'school/search.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class SalaryView(View):
    template_name = 'school/show_count.html'

    def get(self, request, *args, **kwargs):
        d1 = datetime.datetime.now()
        students = StudentNormalSerializer(
            Student.objects.prefetch_related('teachers').filter(
            teachers__salary__gt=1200000
        ).distinct(), many=True)
        count = 0
        teachers_id = []
        total_salary = 0
        for student in students.data:
            count += 1
            for tch in student['teachers']:
                if not tch in teachers_id:
                    teachers_id.append(tch)
        total_salary = Teacher.objects.filter(id__in=teachers_id).aggregate(Sum('salary'))
        context = {
            'student_count': count,
            'total_salary': total_salary['salary__sum']
        }
        return render(request, self.template_name, context)

class TeacherWithMoreSubjectView(View):
    template_name = 'school/show_count.html'

    def get(self, request, *args, **kwargs):
        teachers = Teacher.objects.annotate(subject_count=Count('subjects')).filter(subject_count__gt=1)
        stundents_count = Student.objects.filter(teachers__in=teachers).distinct().count()
        total_hours = 0
        teachers_count = 0
        subjects_id = [] 
        serializer = TeacherSerializer(teachers, many=True)
        for teacher in serializer.data:
            teachers_count += 1
            for sub in teacher['subjects']:
                if not sub['id'] in subjects_id:
                    total_hours += sub['total_duration_min']
                    subjects_id.append(sub['id'])
        context = {
            'students_count': stundents_count,
            'teachers_count': teachers_count,
            'total_hours': total_hours / 60
        }
        return render(request, self.template_name, context)

def teacher_fetch_view(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        data = {}
        if name:
            students = StudentNormalSerializer(
                Student.objects.prefetch_related(
                    'teachers'
                ).filter(teachers__name__icontains=name).distinct(),
                many=True
            )
            student_list = []
            for student in students.data:
                obj = {
                    'Roll No': student['roll_no'],
                    'Name': student['name'],
                    'Date of Join': student['doj'],
                    'Standard': student['standard'],
                    'Ranking': student['ranking']
                }
                student_list.append(obj)
            data = {'result': student_list}
        return JsonResponse(data, safe=False)

