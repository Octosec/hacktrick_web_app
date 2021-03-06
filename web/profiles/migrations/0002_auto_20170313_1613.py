# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 16:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import profiles.utils


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instructor',
            options={'verbose_name': 'Eğitmen', 'verbose_name_plural': 'Eğitmenler'},
        ),
        migrations.AlterField(
            model_name='instructor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='instructor/', validators=[profiles.utils.validate_avatar_dimensions], verbose_name='Resim'),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='institution',
            field=models.CharField(max_length=100, verbose_name='Kuruö'),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Başlık'),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='instructor', related_query_name='instructor', to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.SmallIntegerField(choices=[(0, 'Süperuser'), (1, 'Moderatör'), (2, 'Eğitmen'), (3, 'Katılımcı')], default=3, verbose_name='user tipi'),
        ),
    ]
