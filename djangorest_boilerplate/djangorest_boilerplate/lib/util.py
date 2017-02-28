from django.core.mail import send_mail
from constants import SENDER_EMAIL
from celery import shared_task

@shared_task
def send_password_reset_email(reset_link, receiver_email_list):
	send_mail(
    'Password Reset',
    'Please click this link to reset your password '+reset_link,
    SENDER_EMAIL,
    receiver_email_list,
    fail_silently=False,
	)