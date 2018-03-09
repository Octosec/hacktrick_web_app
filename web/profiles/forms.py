# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils import timezone
from django.forms.models import ModelForm, ModelChoiceField
from django.forms.widgets import TextInput, Textarea, NumberInput, URLInput, Select
from django import forms

from nocaptcha_recaptcha.fields import NoReCaptchaField
from ckeditor.widgets import CKEditorWidget

from .models import Profile, Instructor
from hacktrick.models import Ticket, TicketComment, Training, TrainingDocument, UserTraining, Setting


class UserProfileForm(ModelForm):
    captcha = NoReCaptchaField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'institution', 'phone_number']

        widgets = {
            'first_name': TextInput(attrs={'placeHolder': 'İsim'}),
            'last_name': TextInput(attrs={'placeHolder': 'Soyisim'}),
            'institution': TextInput(attrs={'placeHolder': 'Kurum/Üniversite'}),
            'phone_number': TextInput(attrs={'placeHolder': 'Telefon numarası(+90 000 000 00 00)'}),
        }
        labels = {
            'institution': 'Kurum/Üniversite',
            'phone': 'Telefon'
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['institution'].required = True
        self.fields['phone_number'].required = True


class InstructorForm(ModelForm):
    captcha = NoReCaptchaField()

    class Meta:
        model = Instructor
        fields = ['title', 'institution', 'image', 'facebook', 'twitter', 'linkedin']

        widgets = {
            'institution': TextInput(),
            'title': TextInput(),
            'facebook': TextInput(),
            'twitter': TextInput(),
            'linkedin': TextInput(),
        }


class TicketForm(ModelForm):
    captcha = NoReCaptchaField()

    class Meta:
        model = Ticket
        fields = ['title', 'content']

        widgets = {
            'title': TextInput(attrs={'placeHolder': 'Başlık'}),
            'content': Textarea(attrs={'placeHolder': 'İçerik', 'style': 'width:100% !important;'}),
        }

    def save(self, user=None, commit=True):
        instance = super(TicketForm, self).save(commit=False)
        instance.user = user
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(TicketForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TicketForm, self).clean()
        if Ticket.objects.filter(user=self.request.user).count() >= 5:
            raise ValidationError("Bir kullanıcı 5'den fazla soru soramaz.")
        return cleaned_data


class TicketCommentForm(ModelForm):
    captcha = NoReCaptchaField()

    class Meta:
        model = TicketComment
        fields = ['comment']

        widgets = {
            'comment': Textarea(attrs={'placeHolder': 'Yorum yap', 'style': 'width:100% !important;'}),
        }

    def __init__(self, *args, **kwargs):
        self.ticket = kwargs.pop('ticket')
        super(TicketCommentForm, self).__init__(*args, **kwargs)

    def save(self, user=None, ticket=None, commit=True):
        instance = super(TicketCommentForm, self).save(commit=False)
        instance.user = user
        instance.ticket = ticket
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super(TicketCommentForm, self).clean()
        comment_count = TicketComment.objects.filter(ticket=self.ticket).count()
        if not self.ticket.ticket_status:
            raise ValidationError("Bu soru moderatör tarafından kapatıldığı için yorum yapamazsınız.")
        elif comment_count == 0:
            raise ValidationError("Cevap verilmeyen bir soruya yorum yapamazsınız. "
                                  "Lütfen moderatörün cevap vermesini bekleyin.")
        elif comment_count >= 5:
            raise ValidationError("Bir soruya 5'dan fazla yorum eklenemez.")
        return cleaned_data


class TrainingUpdateForm(ModelForm):
    captcha = NoReCaptchaField()
    content = CharField(widget=CKEditorWidget(config_name='filtered'))

    class Meta:
        model = Training
        fields = ['title', 'content', 'capacity', 'date']

        widgets = {
            'title': TextInput(),
            'capacity': NumberInput(),
            'date': TextInput(),
        }


class DocumentForm(ModelForm):
    captcha = NoReCaptchaField()

    class Meta:
        model = TrainingDocument
        fields = ['name', 'document_url']

        widgets = {
            'name': TextInput(attrs={'placeHolder': 'Döküman adı'}),
            'document_url': URLInput(attrs={'placeHolder': 'Döküman URLi'})
        }

    def save(self, training=None, commit=True):
        instance = super(DocumentForm, self).save(commit=False)
        instance.training = training
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super(DocumentForm, self).clean()
        training_count = TrainingDocument.objects.filter(training=self.training).count()
        if training_count >= 10:
            raise ValidationError('Bir eğitime en fazla 10 döküman eklenebilir.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.training = kwargs.pop('training')
        super(DocumentForm, self).__init__(*args, **kwargs)


class TrainingSelectForm(forms.Form):
    captcha = NoReCaptchaField()
    training_first = ModelChoiceField(
        queryset=None,
        widget=Select(attrs={'id': 'country'})
    )
    agreement = forms.BooleanField(label="Okudum, Anladım",widget=forms.CheckboxInput(attrs={}))

    def __init__(self, *args, **kwargs):
        super(TrainingSelectForm, self).__init__(*args, **kwargs)
        date_setting = Setting.objects.only('training_finish_date').get()
        training_list = []
        for i in Training.objects.all():
            if i.limitless is True and date_setting.training_finish_date >= timezone.localtime(timezone.now()).date():
                training_list.append(i.id)
            elif i.limitless is False and UserTraining.objects.filter(first_selection=i).count() < (
                    i.capacity * 2) and date_setting.training_finish_date >= timezone.localtime(timezone.now()).date():
                training_list.append(i.id)
        self.fields['training_first'].queryset = Training.objects.filter(pk__in=training_list)
        self.fields['training_first'].empty_label = 'Almak istediğiniz eğitimi seçiniz.'
