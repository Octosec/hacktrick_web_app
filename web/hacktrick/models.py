# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from main.declarations import SPONSOR_CATEGORY, MAIL_TYPES
from hacktrick.tasks import send_email_for_information
from profiles.models import Profile, Instructor
from .utils import (
    validate_sponsor_image_dimensions,
    validate_speaker_image_dimensions,
    validate_training_image_dimensions,
)
from .utils import validate_contributor_image_dimensions

from ckeditor.fields import RichTextField


@python_2_unicode_compatible
class Sponsor(models.Model):
    name = models.CharField("İsim", max_length=100)
    category = models.SmallIntegerField("Kategori", choices=SPONSOR_CATEGORY)
    image = models.ImageField(
        "Logo",
        upload_to='sponsor/',
        help_text='372x191',
        validators=[validate_sponsor_image_dimensions]
    )
    order = models.PositiveIntegerField("Sıralama")
    website = models.URLField("Websitesi")

    class Meta:
        verbose_name_plural = "Sponsorlar"
        verbose_name = "Sponsor"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Contributor(models.Model):
    full_name = models.CharField("Ad sayad", max_length=50)
    image = models.ImageField(
        'Resim',
        upload_to='contributor/',
        validators=[validate_contributor_image_dimensions]
    )
    title = models.CharField('Başlık', max_length=100)
    mission = models.CharField('Görev', max_length=100)
    status = models.BooleanField('Durum')
    twitter = models.CharField(
        'Twitter',
        max_length=50,
        help_text='Kullanıcı adı',
        blank=True
    )
    linkedin = models.CharField(
        'Linkedin',
        blank=True,
        max_length=50,
        help_text='Kullanıcı adı'
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "Katkıda bulunanlar"
        verbose_name = "Katkıda bulunan"


@python_2_unicode_compatible
class FAQ(models.Model):
    question = models.CharField('Soru', max_length=300)
    answer = RichTextField('Cevap')
    order = models.PositiveIntegerField('Sıralama')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Sıkça Sorulan Sorular"
        verbose_name = "Soru"


@python_2_unicode_compatible
class Speaker(models.Model):
    full_name = models.CharField('Ad soyad', max_length=60)
    image = models.ImageField(
        'Resim',
        upload_to='speaker/',
        help_text="160x160",
        validators=[validate_speaker_image_dimensions]
    )
    title = models.CharField('Başlık', max_length=100)
    institution = models.CharField('Kurum', max_length=100)
    facebook = models.CharField(help_text='facebook kullanıcı adı',
                                max_length=50, blank=True)
    twitter = models.CharField(help_text='twitter kullanıcı adı',
                               max_length=50, blank=True)
    linkedin = models.CharField(help_text='linkedin kullanıcı adı',
                                max_length=50, blank=True)
    is_visible = models.BooleanField("Görülebilir", default=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "Konuşmacılar"
        verbose_name = "Konuşmacı"


@python_2_unicode_compatible
class ConferenceSlot(models.Model):
    date = models.DateField("Tarih", unique=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name_plural = "Konferans Slotları"
        verbose_name = "Konferans Slotu"


@python_2_unicode_compatible
class Speak(models.Model):
    slot = models.ForeignKey(
        ConferenceSlot,
        verbose_name='Tarih',
        related_name='speaks',
        related_query_name='speak'
    )
    title = models.CharField("Başlık", max_length=150)
    hall = models.CharField('Salon', max_length=100)
    starting_time = models.TimeField("Başlangıç zamanı")
    ending_time = models.TimeField("Bitiş zamanı")
    speaker = models.ForeignKey(
        Speaker,
        verbose_name='Konuşmacı',
        related_query_name='speak',
        related_name='speaker'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Konuşmalar"
        verbose_name = "Konuşma"


@python_2_unicode_compatible
class Training(models.Model):
    title = models.CharField('Başlık', max_length=200)
#    cover_image = models.ImageField(
#        'Resim',
#        upload_to='training/',
#        help_text='770×420',
#        validators=[validate_training_image_dimensions]
#    )
    content = RichTextField('İçerik', config_name='filtered')
    capacity = models.PositiveIntegerField('Kontenjan')
#    reserve_quota = models.PositiveIntegerField('Ek kontenjan')
    date = models.CharField('Tarih', max_length=20)
#    status = models.BooleanField('Durum', default=False)
    instructor = models.ManyToManyField(
        Instructor,
        verbose_name='Eğitmen',
        related_name='trainings',
        related_query_name='training'
    )

    class Meta:
        verbose_name_plural = "Eğitimler"
        verbose_name = "Eğitim"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            training = Training.objects.get(pk=self.pk)
            mail_list = list(Profile.objects.filter(
                user_training__accepted_selection=training).values_list(
                'email', flat=True))
            extra = "<br/> Eğitim: {}<br/>".format(self.title)
            send_email_for_information.delay(email_type=3, email_to=mail_list,
                                             extra=extra)
        super(Training, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        if self.capacity < 10:
            raise ValidationError("Bir eğitimin kapasitesi 10'dan az olamaz.")
        super(Training, self).clean(*args, **kwargs)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class TrainingDocument(models.Model):
    name = models.CharField('İsim', max_length=100)
    document_url = models.URLField('Site')
    training = models.ForeignKey(
        Training,
        verbose_name='Eğitim',
        related_name='documents',
        related_query_name='document'
    )

    class Meta:
        verbose_name_plural = "Eğitim dökümanları"
        verbose_name = "Eğitim dökümanı"

    def save(self, *args, **kwargs):
        if self.pk is None:
            mail_list = list(Profile.objects.filter(
                user_training__accepted_selection=self.training).values_list(
                'email', flat=True))
            extra = "<br/> Eğitim: {}<br/>".format(self.training.title)
            extra += "Döküman başlığı: {}<br/>".format(self.name)
            extra += "Döküman linki: {}<br/>".format(self.document_url)
            send_email_for_information.delay(email_type=4, email_to=mail_list,
                                             extra=extra)
        super(TrainingDocument, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class UserTraining(models.Model):
    first_selection = models.ForeignKey(
        Training,
        verbose_name='İlk seçim',
        related_name='user_first_trainings',
        related_query_name='user_first_training',
        null=True
    )
    accepted_training = models.BooleanField(
        verbose_name='Eğitim Onayı',
        default=False,
    )
    user = models.OneToOneField(
        Profile,
        related_name='user_training',
        related_query_name='user_training',
        verbose_name='Katılımcı',
    )

    class Meta:
        verbose_name_plural = "Katılımcı eğitim"
        verbose_name = "Katılımcı eğitim"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            user_training = UserTraining.objects.get(pk=self.pk)
            if not self.accepted_training and user_training.first_selection != self.first_selection:
                extra = "<br/>Seçilen eğitim: {} <br/>".format(
                    self.first_selection.title)
                send_email_for_information.delay(email_type=1,
                                                 email_to=[self.user.email],
                                                 extra=extra)
            if self.accepted_training:
                extra = "<br/>Eğitiminiz onaylanmıştır. <br/>"
                extra += "<br/>Onaylanan eğitim: {}<br/>".format(
                    self.first_selection.title)
                send_email_for_information.delay(email_type=2,
                                                 email_to=[self.user.email],
                                                 extra=extra)

            if self.user_status and self.user_status != user_training.user_status:
                extra = "<br/>Katılımcı: {}<br/>".format(
                    self.user.get_full_name())
                send_email_for_information.delay(email_type=6,
                                                 email_to=[self.user.email],
                                                 extra=extra)

        super(UserTraining, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        if not self.first_selection.status:
            raise ValidationError('Onaylanmamış eğitim seçemezsiniz.')
        super(UserTraining, self).clean(*args, **kwargs)

    def get_first_selection_title(self):
        return self.first_selection.title if self.first_selection else ''

    def get_username(self):
        return self.user.username


@python_2_unicode_compatible
class Ticket(models.Model):
    title = models.CharField('Başlık', max_length=100)
    content = models.TextField('İçerik')
    status = models.BooleanField('Durum', default=True)
    ticket_status = models.BooleanField('Cevaplanabilirlik', default=True)
    date = models.DateTimeField('Tarih', auto_now_add=True)
    user = models.ForeignKey(
        Profile,
        verbose_name='Katılımcı',
        related_name='tickets',
        related_query_name='ticket'
    )

    class Meta:
        verbose_name_plural = "Sorular"
        verbose_name = "Soru"

    def save(self, *args, **kwargs):
        if self.pk is None:
            mail_list = list(
                Profile.objects.filter(user_type=1).values_list('email',
                                                                flat=True))
            print(mail_list)
            extra = '<br/>Katılımcı: {}'.format(self.user.get_full_name())
            extra += '<br/>Soru: {}'.format(self.title)
            send_email_for_information.delay(email_type=7, email_to=mail_list,
                                             extra=extra)
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return self.content


@python_2_unicode_compatible
class TicketComment(models.Model):
    comment = models.TextField("Yorum")
    date = models.DateTimeField("Tarih", auto_now_add=True)
    user = models.ForeignKey(
        Profile,
        verbose_name='Katılımcı',
        related_name='ticket_comments',
        related_query_name='ticket_comment',
        help_text = 'Otomatik doldurulur'
    )
    ticket = models.ForeignKey(
        Ticket,
        verbose_name='Soru',
        related_name='ticket_comments',
        related_query_name='ticket_comment',
    )

    class Meta:
        ordering = ('date',)
        verbose_name_plural = "Soru yorumları"
        verbose_name = "Soru yorumu"

    def __str__(self):
        return self.comment

    def save(self, *args, **kwargs):
        if self.pk is None:
            extra = "<br/> Soru: {}".format(self.ticket.title)
            send_email_for_information.delay(email_type=8,
                                             email_to=[self.ticket.user.email],
                                             extra=extra)
        super(TicketComment, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Setting(models.Model):
    city = models.CharField('Şehir', max_length=100)
    place_fullname = models.CharField('Konum tam', max_length=150)
    expected_participant = models.PositiveIntegerField(
        'Beklenen katılımcı sayısı')
    expected_speaker = models.PositiveIntegerField('Beklenen konuşmacı sayısı')
    place = models.CharField('Konum kısa',
                             max_length=100,
                             help_text="Anasayfa'da görünmesini istediğiniz şekilde yazınız.")
    date = models.CharField('Tarih',
                            max_length=100,
                            help_text="Anasayfa'da görünmesini istediğiniz şekilde yazınız.")
    starting_date = models.DateTimeField('Başlangıç tarihi')
    address = models.TextField(help_text='Google code')
    live_broadcast = models.TextField(help_text="Html embed code", blank=True)
    about = RichTextField('Hakkında')
    training_note = RichTextField('Eğitim notu')
    cfp = RichTextField("CFP")
    training_selection = models.BooleanField('Eğitim seçimi', default=False)
    participant_selection = models.BooleanField('Katılımcı seçimi',
                                                default=False)
    participant_accept = models.BooleanField('Katılımcı onay', default=False)

    class Meta:
        verbose_name_plural = "Ayarlar"
        verbose_name = "Ayarlar"

    def __str__(self):
        return self.place

    def validate_only_one_instance(self):
        model = self.__class__
        if model.objects.count() > 0 and self.id != model.objects.get().id:
            raise ValidationError("Sadece 1 satır ekleme yapabilisiniz.")

    def clean(self):
        self.validate_only_one_instance()


class Mail(models.Model):
    type = models.SmallIntegerField(
        "Mail seçimi",
        choices=MAIL_TYPES,
        unique=True,
        help_text="İçerik harici kullanıcıya extra bilgiler verilmektedir.")
    title = models.CharField(max_length=300)
    content = RichTextField("İçerik")

    def __str__(self):
        return self.get_type_display()

    class Meta:
        verbose_name_plural = "Mailler"
        verbose_name = "Mail"
