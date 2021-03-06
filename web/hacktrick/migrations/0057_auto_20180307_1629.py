# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-07 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import hacktrick.utils


class Migration(migrations.Migration):

    dependencies = [
        ('hacktrick', '0056_auto_20180306_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugminer',
            name='image',
            field=models.ImageField(help_text='770x420', upload_to='events/', validators=[hacktrick.utils.validate_training_image_dimensions], verbose_name='Resim'),
        ),
        migrations.AlterField(
            model_name='csaward',
            name='image',
            field=models.ImageField(help_text='770x420', upload_to='events/', validators=[hacktrick.utils.validate_training_image_dimensions], verbose_name='Resim'),
        ),
        migrations.AlterField(
            model_name='demoroom',
            name='image',
            field=models.ImageField(help_text='770x420', upload_to='events/', validators=[hacktrick.utils.validate_training_image_dimensions], verbose_name='Resim'),
        ),
        migrations.AlterField(
            model_name='gameofpwners',
            name='image',
            field=models.ImageField(help_text='770x420', upload_to='events/', validators=[hacktrick.utils.validate_training_image_dimensions], verbose_name='Resim'),
        ),
        migrations.AlterField(
            model_name='training',
            name='date',
            field=models.DateField(verbose_name='Eğitim Başlangıç Tarihi'),
        ),
        migrations.AlterField(
            model_name='training',
            name='finish_date',
            field=models.DateField(verbose_name='Eğitim Bitiş Tarihi'),
        ),
    ]
