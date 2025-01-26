from django.shortcuts import render
# HTTPResponse is a class that takes a string as an argument and returns an HTTP response object.
from django.http import HttpResponse

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
def index(request):
    subject = 'Hello, World!'
    html_content = render_to_string('my_mail.html')
    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = 'henkamaroon@goeschman.com'
    msg = EmailMultiAlternatives(subject, html_content, email_from, [email_to])
    msg.attach_alternative(html_content, "text/html")  

    msg.send()

    if msg:
        return HttpResponse('Email sent!')
    else:
        return HttpResponse('Email not sent!')