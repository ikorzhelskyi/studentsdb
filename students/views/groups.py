from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models import Group
from ..util import paginate, get_current_group, DispatchLoginRequired

def groups_list(request):
    """Returns page with list of groups."""
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        groups = Group.objects.filter(id=current_group.id)
    else:
        # otherwise show all groups
        groups = Group.objects.all()

    # try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()
    else:
        order_by = 'title'
        groups = groups.order_by(order_by)

    # paginate groups
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results.
        groups = paginator.page(paginator.num_pages)
    return render(request, 'students/groups_list.html',
                  {'groups': groups})

class GroupForm(ModelForm):
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # add form or edit form
        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False

        # set form tag attributes
        if add_form:
            self.helper.form_action = reverse('groups_add')
        else:
            self.helper.form_action = reverse('groups_edit',
                kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        if add_form:
            submit = Submit('add_button', _(u"Add"),
                            css_class="btn btn-primary")
        else:
            submit = Submit('save_button', _(u"Save"),
                            css_class="btn btn-primary")
        self.helper.layout[-1] = FormActions(
            submit,
            Submit('cancel_button', _(u"Cancel"), css_class="btn btn-link"),
        )

        self.fields['leader'].queryset =\
             self.instance.student_set.order_by('last_name')

    def clean_leader(self):
        """ Check if leader is in the same group """
        new_leader = self.cleaned_data['leader']
        if hasattr(new_leader, 'student_group') and new_leader.student_group != self.instance:
            raise ValidationError(_(u"Student is not in this group!"),
                                   code='invalid')
        return new_leader

class BaseGroupFormView(object):

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('groups'),
                                          _(u"Changes saved successfully!"))

    def post(self, request, *args, **kwargs):
        # handle cancel button
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('groups') +
                u'?status_message=%s' % _(u"Changes canceled."))
        else:
            return super(BaseGroupFormView, self).post(
                request, *args, **kwargs)

class GroupAddView(DispatchLoginRequired, BaseGroupFormView, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'

class GroupUpdateView(DispatchLoginRequired, BaseGroupFormView, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'

class GroupDeleteView(DispatchLoginRequired, BaseGroupFormView, DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'