# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError


def validate_sponsor_image_dimensions(image):
    w, h = get_image_dimensions(image)
    if w != 372 and h != 191:
        raise ValidationError("Resim boyutu 370x190 olmalıdır.")


def validate_speaker_image_dimensions(image):
    w, h = get_image_dimensions(image)
    if w != 160 and h != 160:
        raise ValidationError("Resim boyutu 160x160 olmalıdır.")


def validate_training_image_dimensions(image):
    w, h = get_image_dimensions(image)
    if w != 770 and h != 420:
        raise ValidationError("Resim boyutu 770x420 olmalıdır.")