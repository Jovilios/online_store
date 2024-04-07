from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_greeting_email(email):
    subject = 'Welcome to X Shop!'
    message = 'Hello,\n\nWelcome to our platform! We\'re thrilled to have you on board.\n\nBest regards,\nX Shop Team'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
