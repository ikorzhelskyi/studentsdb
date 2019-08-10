from django.shortcuts import render
from django import forms

class ContactForm(form.Form)
    from_email = forms.EmailField(
        label=u"Ваша Емейл Адреса")

    subject = forms.CharField(
        label=u"Заголовок листа",
        max_length=128)

    message = forms.CharField(
        label=u"Текст повідомлення",
        max_length=2560,
        widget=forms.Textarea)

def contact_admin(request):
    return render(request, 'contact_admin/form.html', {})