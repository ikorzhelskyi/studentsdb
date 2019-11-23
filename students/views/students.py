from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm, ValidationError
from django.views.generic import UpdateView, DeleteView
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from PIL import Image

from ..models import Student, Group
from ..util import paginate, get_current_group, DispatchLoginRequired

def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        order_by = 'last_name'
        students = students.order_by(order_by)

#    # paginate students
#    paginator = Paginator(students, 3)
#    page = request.GET.get('page')
#    try:
#        students = paginator.page(page)
#    except PageNotAnInteger:
#        # If page is not an integer, deliver first page.
#        students = paginator.page(1)
#    except EmptyPage:
#        # If page is out of range (e.g. 9999), deliver last page of results.
#        students = paginator.page(paginator.num_pages)
#
#    return render(request, 'students/students_list.html',
#        {'students': students})

    # implement pagination without 'paginator'
    # count of pages:
    num_rows_per_page = 3
    if len(students):
        num_pages = len(students) // num_rows_per_page
    else:
        num_pages = 1
    # if len(students) % num_rows_per_page > 0
    if len(students) % num_rows_per_page:
        num_pages += 1
    page = request.GET.get('page')
    # check if page is integer
    try:
        page = int(page)
    except:
        page = 1
    # if page is out of range return last page
    if page > num_pages:
        page = num_pages
    elif page < 1:
        page = 1
    students = students[ (page-1)*num_rows_per_page : page*num_rows_per_page ]
    page_list = [p+1 for p in range(num_pages)]
    return render(request, 'students/students_list.html',
            {'students':students,
            'page':page,
            'num_pages':num_pages,
            'num_rows_per_page':num_rows_per_page,
            'page_list':page_list}
            )

@login_required
def students_add(request):
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:
            # errors collection
            errors = {}
            # data for student object
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}
            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = _(u"First Name field is required")
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = _(u"Last Name field is required")
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = _(u"Birthday is required")
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = \
                        _(u"Please, enter correct date format "
                          "(e.g. 1984-12-30)")
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = _(u"Ticket number is required")
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = _(u"Please, select group")
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = _(u"Please, select correct group")
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                try:
                    img = Image.open(photo)
                    file_size = request.FILES['photo'].size

                    if img.format in ('JPG', 'JPEG', 'PNG', 'BMP'):
                        if file_size < 2097152:
                            data['photo'] = photo
                        else:
                            errors['photo'] = _(u'Image file size cannot exceed 2MB')
                    else:
                        errors['photo'] = _(u'Invalid image format.'
                            'Please, upload in one of the formats:'
                            ' *.jpg, *.jpeg, *.png or *.bmp')
                except Exception:
                    errors['photo'] = (u'Invalid image format.'
                        'Please, upload in one of the formats:'
                        ' *.jpg, *.jpeg, *.png or *.bmp')

            # save student
            if not errors:
                # create student object
                student = Student(**data)
                student.save()

                # redirect to students list
                return HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse('home'),
                    _(u"Student added successfully!")))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title'),
                     'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(
                u'%s?status_message=%s' % (reverse('home'),
                _(u"Student addition canceled!")))
    else:
        # initial form render
        return render(request, 'students/students_add.html',
            {'groups': Group.objects.all().order_by('title')})

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', _(u'Save'), css_class="btn btn-primary"),
            Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"),
        )

    def clean_student_group(self):
        """Check if student is leader in any group.
        If yes, then ensure it's the same as selected group."""
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and \
            self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Student is leader of another group.',
                code='invalid')
        return self.cleaned_data['student_group']

class StudentUpdateView(DispatchLoginRequired, UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'),
            _(u"Student updated successfully!"))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=%s' % (reverse('home'),
                _(u"Student update canceled!")))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)

class StudentDeleteView(DispatchLoginRequired, DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'),
            _(u"Student deleted successfully!"))