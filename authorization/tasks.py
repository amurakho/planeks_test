from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.template.loader import render_to_string
from celery import shared_task
from django.core.mail import EmailMessage


@shared_task()
def send_email(to_email, user_key=None, user_id=None, message=None):
    """
        If you want to send message without html - you should pass 'message' arg
        else it will send html-message with static text
    """
    from_email = settings.ADMIN_EMAIL
    if message:
        msg = EmailMessage(subject='Confirm register', body=message, from_email=from_email, bcc=[to_email])
    else:
        msg_html = render_to_string('registration/confirm_email.html',
                                    {'key': user_key, 'domain': settings.SITE_URL,
                                     'id': user_id})
        msg = EmailMessage(subject='Confirm register', body=msg_html, from_email=from_email, bcc=[to_email])
        msg.content_subtype = "html"
    msg.send()



