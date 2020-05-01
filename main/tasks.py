from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task()
def send_email_about_comment(to_email, pub_url):
    """
        send message about comment to author
    """
    from_email = settings.ADMIN_EMAIL
    message = """
    Someone write comment to your pub
    Check it:
        {}   
    """.format(pub_url)
    msg = EmailMessage(subject='Comment!', body=message, from_email=from_email, bcc=[to_email])
    msg.send()


