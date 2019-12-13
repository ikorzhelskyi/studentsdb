from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView, TemplateView

from students.views.students import StudentUpdateView, StudentDeleteView
from students.views.groups import GroupAddView, GroupUpdateView, \
    GroupDeleteView, groups_list
from students.views.journal import JournalView
from stud_auth.views import UsersListView, UserDetailView, UserUpdateView
from registration.backends.default import views as registration_views

from .settings import MEDIA_ROOT, DEBUG


js_info_dict = {
    'packages': ('students',),
}

urlpatterns = patterns('',
    # Students urls
    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/$', 'students.views.students.students_add',
         name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(),
         name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(),
         name='students_delete'),

    # Groups urls
    url(r'^groups/$', login_required(groups_list), name='groups'),
    url(r'^groups/add/$', login_required(GroupAddView.as_view()),
         name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', login_required(GroupUpdateView.as_view()),
         name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', login_required(GroupDeleteView.as_view()),
         name='groups_delete'),

    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    # User Related urls
    url(r'^users/profile/$', login_required(TemplateView.as_view(
        template_name='registration/profile.html')), name='profile'),
    url(r'^users/profiles/$', login_required(UsersListView.as_view()),
        name='users_list'),
    url(r'^users/profile/(?P<pk>\d+)/$', login_required(UserDetailView.as_view()),
        name='user_profile'),
    url(r'^users/profile/edit/$', login_required(UserUpdateView.as_view()),
        name='user_profile_edit'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'},
        name='auth_logout'),
    url(r'^users/register/complete/$', TemplateView.as_view(
        template_name='registration/registration_complete.html'),
        name='registration_complete'),
    url(r'^users/activate/complete/$',
        TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(r'^users/password_reset/$', auth_views.password_reset,
        name='auth_password_reset'),
    url(r'^users/register/$', registration_views.RegistrationView.as_view(),
        name='registration_register'),
    url(r'^users/activate/(?P<activation_key>\w+)/$',
        registration_views.ActivationView.as_view(),
        name='registration_activate'),
    url(r'^users/password_reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^users/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^users/reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^users/password_change/$', auth_views.password_change,
        name='password_change'),
    url(r'^users/password_change/done/$',
        RedirectView.as_view(pattern_name='profile'),
        name='password_change_done'),
    url(r'^users/', include('registration.backends.default.urls', namespace='users')),
    #url(r'^users/', include('registration.backends.simple.urls',
    #    namespace='users')),

    # Social Auth Related urls
    url('^social/', include('social.apps.django_app.urls', namespace='social')),

    # Contact Admin Form
    url(r'^contact-admin/$', 'students.views.contact_admin.contact_admin',
        name='contact_admin'),

    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # View for set language
    url('^set-language/$',
        'students.views.set_language.set_language', name='set_language'),

    url(r'^admin/', include(admin.site.urls)),

)

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))