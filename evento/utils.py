from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import re
from django.utils.text import slugify
import math, random
from datetime import datetime, timedelta
from django.utils import timezone

def generateOTP():
    digits = "0123456789"
    OTP = ""

    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def now_plus_5_minutes():
    return datetime.now() + timezone.timedelta(minutes=5)

class Validate:
    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def validate_password(self):
        if len(self.password) < 6:
            resp = 'password field must be more than 6 characters'

        elif not re.search("[a-z]", self.password):
            resp = 'password field must contain atleast 1 lowercase letter'

        elif not re.search("[A-Z]", self.password):
            resp = 'password field must contain atleast 1 uppercase letter'

        elif not re.search("[0-9]", self.password):
            resp = 'password field must contain atleast 1 digit'

        elif not re.search("[_@$#!*]", self.password):
            resp = 'password field must contain one of the following characters _ @ $ # ! *'

        else:
            resp = True
        return resp

    def validate_email(self):
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", self.email):
            resp =  False
        else:
            resp = True
        return resp


def send_email(subject, mail_from, to_emails, template, data):

    subject = subject
    html_message = render_to_string(template, {'data': data})
    plain_message = strip_tags(html_message)

    from_email = 'Evento <{}>'.format(mail_from)
    send_mail = mail.send_mail(subject, plain_message, from_email, to_emails, html_message=html_message, fail_silently=False)

    return send_mail

def unique_slug_generator(model_instance, title, slug_field):
    slug = slugify(title)
    model_class = model_instance.__class__

    while model_class._default_manager.filter(slug=slug).exists():
        object_pk = model_class._default_manager.latest('pk')
        object_pk = object_pk.pk + 1
        slug = f'{slug}-{object_pk}'

    return slug
