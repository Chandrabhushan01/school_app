"""school_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from school.views import ClassRoomView, TeacherSearchView
from school.views import teacher_fetch_view, SalaryView
from school.views import TeacherWithMoreSubjectView, IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', IndexView.as_view(), name='index'),
    url(r'^classroom/$', ClassRoomView.as_view(), name='classroom'),
    url(r'^teacher-search/$', TeacherSearchView.as_view(), name='teacher-search'),
    url(r'^search/$', teacher_fetch_view, name='search'),
    url(r'^total-salary/$', SalaryView.as_view(), name='salary'),
    url(r'^subjects/$', TeacherWithMoreSubjectView.as_view(), name='subjects'),
]

