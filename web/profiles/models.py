from django.contrib.auth.models import AbstractUser
from django.db import models

from main.declarations import USER_TYPES


class Profile(AbstractUser):
    user_type = models.SmallIntegerField(choices=USER_TYPES, default=3)
    email = models.EmailField('email address', unique=True)
    registered_ip = models.GenericIPAddressField(blank=True, null=True)

    def __unicode__(self):
        return self.username
