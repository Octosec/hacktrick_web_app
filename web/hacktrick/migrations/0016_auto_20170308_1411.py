# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hacktrick', '0015_auto_20170308_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='instructor',
            field=models.ManyToManyField(related_name='trainings', related_query_name='training', to='profiles.Instructor'),
        ),
    ]
