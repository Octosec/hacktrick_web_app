from django.db.models.signals import pre_delete, m2m_changed, post_save, pre_save
from django.dispatch import receiver
from hacktrick.models import Training
from hacktrick.tasks import send_email_for_information

@receiver(m2m_changed, sender=Training.instructor.through)
def training_instructor_change(sender, instance, action, **kwargs):
    extra = "<br/>Eğitim: {}".format(instance.title)
    for instructor in instance.instructor.all():
        if action == "pre_remove":
            send_email_for_information.delay(
                email_type=10,
                email_to=[instructor.user.email],
                extra=extra)
        elif action == "post_add":
            send_email_for_information.delay(
                email_type=9,
                email_to=[instructor.user.email],
                extra=extra)