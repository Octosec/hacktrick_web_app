# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms.models import ModelForm
from django.forms.widgets import TextInput

from .models import Profile, Instructor


class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['institution', 'phone_number']

        widgets = {
            'institution': TextInput(attrs={'placeHolder': 'Kurum/Üniversite'}),
            'phone_number': TextInput(attrs={'placeHolder': 'Telelfon numarası(+90 000 000 00 00)'}),
        }
        labels = {
            'institution': 'Kurum/Üniversite',
            'phone': 'Telefon'
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['institution'].required = True
        self.fields['phone_number'].required = True


class InstructorForm(ModelForm):
    class Meta:
        model = Instructor
        fields = ['title', 'institution', 'image', 'facebook', 'twitter', 'linkedin']

        widgets = {
            'institution': TextInput(attrs={'placeHolder': 'Kurum/Üniversite'}),
            'title': TextInput(attrs={'placeHolder': 'Ünvan'}),
            'facebook': TextInput(attrs={'placeHolder': 'Facebook kullanıcı adı'}),
            'twitter': TextInput(attrs={'placeHolder': 'Twitter kullanıcı adı'}),
            'linkedin': TextInput(attrs={'placeHolder': 'Linkedin kullanıcı adı'}),
        }
