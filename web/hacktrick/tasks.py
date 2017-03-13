from __future__ import absolute_import, unicode_literals
import logging
from celery import shared_task
from django.core.mail.message import EmailMultiAlternatives


@shared_task(queue='default')
def send_email_for_information(email_type, email_to, extra):
    try:
        from .models import Mail
        mail_object = Mail.objects.get(type=email_type)
        content = mail_object.content + extra
        content += "<br/><br/><a href='http://www.hacktrickconf.com'>http://www.hacktrickconf.com</a>"
        content += "Hacktrick Organizasyon Ekibi"
        subject, email_from = mail_object.title, "noreply@hacktrickconf.com"
        mail_send = EmailMultiAlternatives(mail_object.title, content, email_from, email_to)
        mail_send.attach_alternative(content, "text/html")
        mail_send.send()
    except Exception as e:
        logging.error('There was some error when sending email: {}'.format(e), exc_info=True)
