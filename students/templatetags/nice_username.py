from django import template

register = template.Library()

@register.filter
def nice_username(user):
    """Returns string: 'full name', or if don't exists, 'username' """
    name = user.get_full_name()
    if not name:
        name = user.username
    return name