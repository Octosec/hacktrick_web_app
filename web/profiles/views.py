from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormMixin
from django.views.generic.list import ListView
from django.contrib import messages

from .mixins import InstructorRequiredMixin, InfoRequiredMixin
from .forms import UserProfileForm, InstructorForm, TicketForm, TicketCommentForm
from .models import Profile, Instructor
from hacktrick.models import Ticket


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


class TicketListView(LoginRequiredMixin, InfoRequiredMixin, FormMixin, ListView):
    model = Ticket
    template_name = 'pages/profile/tickets.html'
    form_class = TicketForm
    success_message = 'Soru başarı ile gönderildi. İnceledikten sonra yanıt vereceğiz.'

    def get_queryset(self):
        return Ticket.objects.filter(status=True, user=self.request.user)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save(user=self.request.user)
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(TicketListView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(form=form, object_list=self.object_list)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('profiles:tickets')

    def get_form_kwargs(self):
        kwargs = super(TicketListView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs


class TicketDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Ticket
    template_name = 'pages/profile/ticket_detail.html'
    form_class = TicketCommentForm
    success_message = 'Yorum başarı ile eklendi.'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save(user=self.request.user, ticket=self.get_object())
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(TicketDetailView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(form=form, object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('profiles:ticket_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        try:
            return Ticket.objects.get(user=self.request.user, status=True, pk=self.kwargs['pk'])
        except:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super(TicketDetailView, self).get_form_kwargs()
        kwargs.update({
            'ticket': self.get_object()
        })
        return kwargs

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse_lazy('hacktrick:index'))
