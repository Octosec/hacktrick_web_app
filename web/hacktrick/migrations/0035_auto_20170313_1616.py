# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hacktrick', '0034_auto_20170313_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='linkedin',
            field=models.CharField(blank=True, help_text='Kullanıcı adı', max_length=50, verbose_name='Linkedin'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='twitter',
            field=models.CharField(blank=True, help_text='Kullanıcı adı', max_length=50, verbose_name='Twitter'),
        ),
    ]
