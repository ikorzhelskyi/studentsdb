# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

def journal(request):
    students = (
        {'id': 1,
         'first_name': u'Андрій',
         'last_name': u'Вірт'},
        {'id': 2,
         'first_name': u'Юрій',
         'last_name': u'Семчук'},
        {'id': 3,
         'first_name': u'Роман',
         'last_name': u'Ярощак'},
        )
    return render(request, 'students/journal.html',
        {'students': students})