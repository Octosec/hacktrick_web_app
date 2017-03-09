from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import Http404
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormMixin, DeleteView, FormView
from django.views.generic.list import ListView
from django.contrib import messages

from .mixins import (
    InstructorRequiredMixin,
    InfoRequiredMixin,
    ParticipantRequiredMixin,
    TrainingSelectionRequiredMixin
)

from .forms import (
    UserProfileForm,
    InstructorForm,
    TicketForm,
    TicketCommentForm,
    TrainingUpdateForm,
    DocumentForm,
    TrainingSelectForm
)
from .models import Profile, Instructor
from hacktrick.models import (
    Ticket,
    Training,
    Setting,
    TrainingDocument,
    UserTraining
)


class LoginView(TemplateView):
    template_name = 'pages/profile/login.html'


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'pages/profile/profile.html'
    model = Profile
    success_message = "Bilgiler başarı ile güncellendi."

    def get_initial(self):
        return {
            'institution': self.request.user.institution,
            'phone_number': self.request.user.phone_number
        }

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profiles:profile')


class InstructorView(LoginRequiredMixin, InfoRequiredMixin, InstructorRequiredMixin, UpdateView):
    model = Instructor
    template_name = 'pages/profile/instructor/instructor.html'
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


class TicketDetailView(LoginRequiredMixin, InfoRequiredMixin, FormMixin, DetailView):
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


class TrainingListView(LoginRequiredMixin, InfoRequiredMixin, InstructorRequiredMixin, ListView):
    template_name = 'pages/profile/instructor/trainings.html'
    model = Training

    def get_queryset(self):
        return Training.objects.filter(status=True, instructor=self.request.user.instructor)


class TrainingUpdateView(LoginRequiredMixin, InfoRequiredMixin, InstructorRequiredMixin, UpdateView):
    template_name = 'pages/profile/instructor/training_update.html'
    model = Training
    form_class = TrainingUpdateForm

    def get_context_data(self, **kwargs):
        context = super(TrainingUpdateView, self).get_context_data(**kwargs)
        try:
            context["training_note"] = Setting.objects.get().training_note
        except Setting.DoesNotExist:
            context["training_note"] = ""
        return context

    def get_object(self, queryset=None):
        try:
            return Training.objects.get(
                instructor=self.request.user.instructor,
                status=True,
                pk=self.kwargs['pk']
            )
        except:
            raise Http404

    def get_success_url(self):
        return reverse_lazy('profiles:training_update', kwargs={'pk': self.kwargs['pk']})


class TrainingDocumentListView(LoginRequiredMixin, InfoRequiredMixin, InstructorRequiredMixin, FormMixin, DetailView):
    model = Training
    template_name = 'pages/profile/instructor/training_documents.html'
    training = None
    form_class = DocumentForm
    success_message = 'Dökümana başarı ile eklendi.'

    def get_object(self, queryset=None):
        try:
            return Training.objects.get(
                instructor=self.request.user.instructor,
                status=True,
                pk=self.kwargs['pk']
            )
        except:
            raise Http404

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save(training=self.get_object())
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(TrainingDocumentListView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(form=form, object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('profiles:training_documents', kwargs={'pk': self.kwargs['pk']})


    def get_form_kwargs(self):
        kwargs = super(TrainingDocumentListView, self).get_form_kwargs()
        kwargs.update({
            'training': self.get_object()
        })
        return kwargs


class TrainingDocumentDeleteView(LoginRequiredMixin, InfoRequiredMixin, InstructorRequiredMixin, DeleteView):
    model = TrainingDocument
    template_name = 'pages/profile/instructor/training_document_delete.html'

    def get_object(self, queryset=None):
        obj = super(TrainingDocumentDeleteView, self).get_object()
        if not self.request.user.instructor in obj.training.instructor.all():
            raise Http404
        return obj

    def get_success_url(self):
        training_pk = self.get_object().training.pk
        return reverse_lazy('profiles:training_documents', kwargs={'pk': training_pk})

class ParticipantSelectTrainingView(LoginRequiredMixin, InfoRequiredMixin, ParticipantRequiredMixin,
                                    TrainingSelectionRequiredMixin, FormView):
    template_name = 'pages/profile/participant/select_training.html'
    form_class = TrainingSelectForm
    success_message = "Seçim işleminizi başarı ile gerçekleştirdiniz."

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        first_selection = cleaned_data.get('training_first', None)
        second_selection = cleaned_data.get('training_second', None)
        user_training, _ = UserTraining.objects.get_or_create(user=self.request.user)
        user_training.first_selection = first_selection
        user_training.second_selection = second_selection
        user_training.save()
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(ParticipantSelectTrainingView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profiles:training_select')

    def get_initial(self):
        initial = super(ParticipantSelectTrainingView, self).get_initial()
        try:
            initial['training_first'] = self.request.user.user_training.first_selection
            initial['training_second'] = self.request.user.user_training.second_selection
        except UserTraining.DoesNotExist:
            pass
        return initial

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse_lazy('hacktrick:index'))
