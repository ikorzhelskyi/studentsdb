# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

def students_list(request):
    students = (
        {'id': 1,
         'first_name': u'Андрій',
         'last_name': u'Вірт',
         'ticket': 2501,
         'image': 'img/student_1.jpg'},
        {'id': 2,
         'first_name': u'Юрій',
         'last_name': u'Семчук',
         'ticket': 2548,
         'image': 'img/student_2.jpg'},
        {'id': 3,
         'first_name': u'Роман',
         'last_name': u'Ярощак',
         'ticket': 2557,
         'image': 'img/student_3.jpg'},
        )
    return render(request, 'students/students_list.html',
        {'students': students})

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)