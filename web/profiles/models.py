# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from phonenumber_field.modelfields import PhoneNumberField

from main.declarations import USER_TYPES
from .utils import validate_avatar_dimensions


@python_2_unicode_compatible
class Profile(AbstractUser):
    user_type = models.SmallIntegerField(choices=USER_TYPES, default=3)
    email = models.EmailField('email address', unique=True)
    institution = models.CharField('kurum/üniversite', blank=True, max_length=100)
    phone_number = PhoneNumberField('telefon', blank=True, help_text='format: +905306602321')

    def save(self, *args, **kwargs):
        if self.pk is None:
            # TODO: Send mail
            pass
        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.username


class Instructor(models.Model):
    user = models.OneToOneField(
        Profile,
        related_name='instructor',
        related_query_name='instructor'
    )
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='instructor/',
        blank=True,
        null=True,
        validators=[validate_avatar_dimensions]
    )
    facebook = models.CharField(help_text='facebook kullanıcı adı', max_length=50, blank=True)
    twitter = models.CharField(help_text='twitter kullanıcı adı', max_length=50, blank=True)
    linkedin = models.CharField(help_text='linkedin kullanıcı adı', max_length=50, blank=True)

    def __str__(self):
        return self.user.username

    def clean(self, *args, **kwargs):
        if not self.user.user_type == 2:
            raise ValidationError('Seçtiğiniz kullanıcının tipi eğitmen olmak zorundadır.')
        super(Instructor, self).clean(*args, **kwargs)
