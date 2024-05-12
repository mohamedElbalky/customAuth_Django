from django.core.mail import send_mail
from django.conf import settings


from celery import shared_task


@shared_task
def send_verification_email(user_email, verification_url):
    send_mail(
        subject="Verify your email",
        message=f"Please verify your email by clicking this link: {verification_url}",
        from_email="elbalky4@gmail.com",
        recipient_list=[user_email],
        fail_silently=False,
    )
