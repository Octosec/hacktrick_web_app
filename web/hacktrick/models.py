from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from main.declarations import SPONSOR_CATEGORY
from profiles.models import Profile


@python_2_unicode_compatible
class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    category = models.SmallIntegerField(choices=SPONSOR_CATEGORY)
    image = models.ImageField(upload_to='sponsor/', help_text='370x190')
    order = models.PositiveIntegerField()

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
    url = models.URLField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.question


@python_2_unicode_compatible
class ConferenceSlot(models.Model):
    date = models.DateField()
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()


@python_2_unicode_compatible
class Speaker(models.Model):
    full_name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='speaker/')
    corporate = models.CharField(max_length=100)
    slot = models.ForeignKey(
        ConferenceSlot,
        related_name='speakers',
        related_query_name='speaker'
    )

    def __str__(self):
        return self.full_name


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

    def __str__(self):
        return self.comment


@python_2_unicode_compatible
class Setting(models.Model):
    place = models.CharField(max_length=100)
    starting_date = models.DateTimeField()
    ending_date = models.DateTimeField()
    address = models.TextField(help_text='Google code')

    def __str__(self):
        return self.place
