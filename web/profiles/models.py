from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from phonenumber_field.modelfields import PhoneNumberField

from main.declarations import USER_TYPES


@python_2_unicode_compatible
class Profile(AbstractUser):
    user_type = models.SmallIntegerField(choices=USER_TYPES, default=3)
    email = models.EmailField('email address', unique=True)
    institution = models.CharField('kurum/üniversite', blank=True, max_length=100)
    phone_number = PhoneNumberField('telefon', blank=True, help_text='format: +905306602321')

    def __unicode__(self):
        return self.username
