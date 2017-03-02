from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, UpdateView

from .forms import UserProfileForm
from .models import Profile


class LoginView(TemplateView):
    template_name = 'pages/profile/login.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'pages/profile/profile.html'
    model = Profile

    def get_initial(self):
        return {
            'institution': self.request.user.institution,
            'phone_number': self.request.user.phone_number
        }

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profiles:profile')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse_lazy('hacktrick:index'))
