import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import CustomUser
def sendOTPtOEmail(email,otp):
    subject = " OTP for account login" 
    message = f"""Hi, please use this otp to login
    {otp} """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )