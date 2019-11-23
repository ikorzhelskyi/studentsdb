"""Custom userful utils for student application"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator, classonlymethod
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView


class DispatchLoginRequired(object):
    """Base class for restrict access to views"""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


def paginate(objects, size, request, context, var_name='object_list'):
    """Paginate objects provided by view"""
    # Apply pagination.
    paginator = Paginator(objects, size)
    page = request.GET.get('page', '1')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        object_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        object_list = paginator.page(paginator.num_pages)

    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context

def get_groups(request):
    """Returns list of existing groups"""
    # deferred import of Group model to avoid cycled imports
    from .models import Group

    # get currently selected group
    cur_group = get_current_group(request)

    groups = []
    for group in Group.objects.all().order_by('title'):
        groups.append({
            'id': group.id,
            'title': group.title,
            'leader': group.leader and (u'%s %s' % (group.leader.first_name,
                group.leader.last_name)) or None,
            'selected': cur_group and cur_group.id == group.id and True or False
        })
    return groups

def get_current_group(request):
    """Returns currently selected group or None"""

    # we remember selected group in a cookie
    pk = request.COOKIES.get('current_group')

    if pk:
        from .models import Group
        try:
            group = Group.objects.get(pk=int(pk))
        except Group.DoesNotExist:
            return None
        else:
            return group
    else:
        return None