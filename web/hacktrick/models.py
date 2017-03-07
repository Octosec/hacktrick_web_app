# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from main.declarations import SPONSOR_CATEGORY
from profiles.models import Profile
from .utils import validate_sponsor_image_dimensions, validate_speaker_image_dimensions


@python_2_unicode_compatible
class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    category = models.SmallIntegerField(choices=SPONSOR_CATEGORY)
    image = models.ImageField(
        upload_to='sponsor/',
        help_text='372x191',
        validators=[validate_sponsor_image_dimensions]
    )
    order = models.PositiveIntegerField()
    website = models.URLField()


    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Contributor(models.Model):
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='contributor/')
    title = models.CharField(max_length=100)
    mission = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


@python_2_unicode_compatible
class CFP(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.question


@python_2_unicode_compatible
class Speaker(models.Model):
    full_name = models.CharField('Ad soyad', max_length=60)
    image = models.ImageField(
        'Resim',
        upload_to='speaker/',
        help_text="160x160",
        validators=[validate_speaker_image_dimensions]
    )
    title = models.CharField(max_length=100)
    institution = models.CharField('Kurum', max_length=100)
    facebook = models.CharField(help_text='facebook kullanıcı adı', max_length=50, blank=True)
    twitter = models.CharField(help_text='twitter kullanıcı adı', max_length=50, blank=True)
    linkedin = models.CharField(help_text='linkedin kullanıcı adı', max_length=50, blank=True)

    def __str__(self):
        return self.full_name


@python_2_unicode_compatible
class ConferenceSlot(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)


@python_2_unicode_compatible
class Speak(models.Model):
    slot = models.ForeignKey(
        ConferenceSlot,
        related_name='speaks',
        related_query_name='speak'
    )
    title = models.CharField(max_length=150)
    hall = models.CharField('Salon', max_length=100)
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    speaker = models.ForeignKey(
        Speaker,
        related_query_name='speak',
        related_name='speaker'
    )

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Training(models.Model):
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='training/')
    content = models.TextField()
    capacity = models.PositiveIntegerField()
    reserve_quota = models.PositiveIntegerField()
    instructor = models.ManyToManyField(
        Profile,
        related_name='trainings',
        related_query_name='training'
    )

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class TrainingDocument(models.Model):
    name = models.CharField(max_length=100)
    document = models.FileField(upload_to='document/')
    is_public = models.BooleanField(default=True)
    training = models.ForeignKey(
        Training,
        related_name='documents',
        related_query_name='document'
    )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class UserTraining(models.Model):
    first_selection = models.ForeignKey(
        Training,
        related_name='user_first_trainings',
        related_query_name='user_first_training'
    )
    second_selection = models.ForeignKey(
        Training,
        related_name='user_second_trainings',
        related_query_name='user_second_training'
    )
    accepted_selection = models.ForeignKey(
        Training,
        related_name='user_accepted_trainings',
        related_query_name='user_accepted_training'
    )
    user = models.ForeignKey(
        Profile,
        related_name='user_trainings',
        related_query_name='user_training'
    )


@python_2_unicode_compatible
class Ticket(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        Profile,
        related_name='tickets',
        related_query_name='ticket'
    )

    def __str__(self):
        return self.content


@python_2_unicode_compatible
class TicketComment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        Profile,
        related_name='ticket_comments',
        related_query_name='ticket_comment'
    )
    ticket = models.ForeignKey(
        Ticket,
        related_name='ticket_comments',
        related_query_name='ticket_comment'
    )

    class Meta:
        ordering = ('date', )

    def __str__(self):
        return self.comment


@python_2_unicode_compatible
class Setting(models.Model):
    city = models.CharField('Şehir', max_length=100)
    place_fullname = models.CharField('Konum tam', max_length=150)
    expected_participant = models.PositiveIntegerField('Beklenen katılımcı sayısı')
    expected_speaker = models.PositiveIntegerField('Beklenen konuşmacı sayısı')
    place = models.CharField('Konum kısa',
                             max_length=100,
                             help_text="Anasayfa'da görünmesini istediğiniz şekilde yazınız.")
    date = models.CharField('Tarih',
                            max_length=100,
                            help_text="Anasayfa'da görünmesini istediğiniz şekilde yazınız.")
    starting_date = models.DateTimeField('Başlangıç tarihi')
    address = models.TextField(help_text='Google code')
    about = models.TextField('Hakkında', help_text='HTML kodu yazabilirsiniz.')

    def __str__(self):
        return self.place

    def validate_only_one_instance(self):
        model = self.__class__
        if model.objects.count() > 0 and self.id != model.objects.get().id:
            raise ValidationError("Sadece 1 satır ekleme yapabilisiniz.")

    def clean(self):
        self.validate_only_one_instance()
