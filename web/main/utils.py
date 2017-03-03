# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_avatar_dimensions(image):
    w, h = get_image_dimensions(image)
    if w != 450 and h != 450:
        raise ValidationError("Resim boyutu 450x450 olmalıdır.")
