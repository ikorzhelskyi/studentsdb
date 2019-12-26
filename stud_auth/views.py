from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import StProfile
from .forms import ProfileEditForm

class UsersListView(ListView):
    model = User
    template_name = 'registration/users_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user_info'

class UserUpdateView(SuccessMessageMixin, UpdateView):
    form_class = ProfileEditForm
    template_name = 'registration/profile_edit.html'
    success_message = _(u'Profile successfully updated!')
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        obj, created = StProfile.objects.get_or_create(user=self.request.user)
        return obj