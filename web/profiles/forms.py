from django.forms.models import ModelForm
from django.forms.widgets import TextInput

from .models import Profile


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
