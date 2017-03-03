from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

from .mixins import InstructorRequiredMixin
from .forms import UserProfileForm, InstructorForm
from .models import Profile, Instructor


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


class InstructorView(LoginRequiredMixin, InstructorRequiredMixin, UpdateView):
    model = Instructor
    template_name = 'pages/profile/instructor.html'
    form_class = InstructorForm

    def get_object(self, queryset=None):
        return self.request.user.instructor

    def get_success_url(self):
        return reverse_lazy('profiles:instructor')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse_lazy('hacktrick:index'))
