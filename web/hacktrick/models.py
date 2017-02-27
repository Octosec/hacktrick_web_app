from django.db import models

"""
SPONSOR_CATEGORY = (
    (0, 'Other'),
)


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    category = models.SmallIntegerField(choices=SPONSOR_CATEGORY)
    image = models.ImageField(upload_to='sponsor/')
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Contributor(models.Model):
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='contributor/')
    title = models.CharField(max_length=100)
    mission = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class CFP(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    url = models.URLField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.question


class ConferenceSlot(models.Model):
    date = models.DateField()
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()


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


class Training(models.Model):
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='training/')
    content = models.TextField()
    capacity = models.PositiveIntegerField()
    reserve_quota = models.PositiveIntegerField()

    def __str__(self):
        return self.title


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


"""