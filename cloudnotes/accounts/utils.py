from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone


def send_html_email(subject, template, context, to_email):
    html_content = render_to_string(template, context)

    email = EmailMultiAlternatives(
        subject=subject,
        body="This email requires HTML support.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()