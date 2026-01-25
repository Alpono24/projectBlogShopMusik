from celery import shared_task
from django.conf import settings

from django.core.mail import send_mail


#
@shared_task(name="send_email_async")
def send_email_async(subject, message, recipient_list):
    """
    Задача Celery для обратной связи посетителя сайта по email с админом
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False
        )
    except Exception as e:
        raise e