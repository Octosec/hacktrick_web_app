from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.mail.message import EmailMultiAlternatives
import logging


@shared_task(queue='default')
def send_email(mail_content, html_content, to):
    try:
        subject, email_from = mail_content, ""
        mail_send = EmailMultiAlternatives(subject, mail_content, email_from, to)
        mail_send.attach_alternative(html_content, "text/html")
        mail_send.send()
    except Exception as e:
        logging.error('There was some error when sending email: {}'.format(e), exc_info=True)
