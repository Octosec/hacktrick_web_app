# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError

def validate_avatar_dimensions(image):
    w, h = get_image_dimensions(image)
    if w != 160 and h != 160:
        raise ValidationError("Resim boyutu 160x160 olmalıdır.")
