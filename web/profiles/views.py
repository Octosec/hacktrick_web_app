import codecs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import Http404, HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormMixin, DeleteView, FormView
from django.views.generic.list import ListView
from django.contrib import messages
from django.db.models import Q

from pure_pagination.mixins import PaginationMixin
from .models import Profile, Instructor
from .mixins import (
    InstructorRequiredMixin,
    InfoRequiredMixin,
    ParticipantRequiredMixin,
    TrainingSelectionRequiredMixin,
    ParticipantSelectionRequiredMixin,
    ParticipantTrainingAcceptRequiredMixin
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
from hacktrick.models import (
    Ticket,
    Training,
    Setting,
    TrainingDocument,
    UserTraining
)

import csv


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
        return Ticket.objects.filter(user=self.request.user)

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
            return Ticket.objects.get(user=self.request.user, pk=self.kwargs['pk'])
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
        return Training.objects.filter(instructor=self.request.user.instructor)


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
    error_message = "Onaylanan eğitimi değiştiremezsiniz."

    def get_context_data(self, **kwargs):
        context = super(ParticipantSelectTrainingView, self).get_context_data(**kwargs)
        try:
            section_training = UserTraining.objects.filter(user_id=self.request.user.id).get()
            context['section_training'] = section_training.first_selection
        except UserTraining.DoesNotExist:
            context['section_training'] = False

        try:
            verify_selection = UserTraining.objects.filter(user_id=self.request.user.id, accepted_training=True).get()
            context['verify_selection'] = verify_selection.first_selection
        except UserTraining.DoesNotExist:
            context['verify_selection'] = False
        context['status'] = Setting.objects.only(
            'training_finish_date').get().training_finish_date >= timezone.localtime(timezone.now()).date()
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        first_selection = cleaned_data.get('training_first', None)
        user_training, _ = UserTraining.objects.get_or_create(user=self.request.user)
        user_training.first_selection = first_selection
        if user_training.accepted_training:
            messages.add_message(self.request, messages.ERROR, self.error_message)
        else:
            user_training.save()
            messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(ParticipantSelectTrainingView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profiles:training_select')

    def get_initial(self):
        initial = super(ParticipantSelectTrainingView, self).get_initial()
        try:
            initial['training_first'] = self.request.user.user_training.first_selection
        except UserTraining.DoesNotExist:
            pass
        return initial


class InstructorAcceptParticipantView(LoginRequiredMixin, InfoRequiredMixin, InstructorRequiredMixin,
                                      ParticipantSelectionRequiredMixin, PaginationMixin, ListView):
    template_name = 'pages/profile/instructor/accept_participant.html'
    model = UserTraining
    training = None
    accepted_count = None
    paginate_by = 50
    accepted_count_error_message = 'Kabul ettiğiniz kullanıcı sayısı sınıf kontenjanını aştığı için kabul işlemi gerçekleşmemiştir.'
    multi_submit_error = 'İki işlemi aynı anda yapamazsınız.'

    def dispatch(self, request, *args, **kwargs):
        self.get_training_object()
        self.accepted_count = UserTraining.objects.filter(first_selection=self.training, accepted_training=True).count()
        return super(InstructorAcceptParticipantView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InstructorAcceptParticipantView, self).get_context_data(**kwargs)
        context["accepted_count"] = self.accepted_count
        context["training"] = self.training
        return context

    def get_training_object(self):
        try:
            self.training = Training.objects.get(instructor=self.request.user.instructor, pk=self.kwargs['pk'])
        except Training.DoesNotExist:
            raise Http404

    def get_queryset(self):
        term = self.request.GET.get('search', None)
        query = UserTraining.objects.filter(first_selection=self.training)
        if term:
            query = query.filter(Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term))
        return query.order_by('accepted_training')

    def post(self, request, *args, **kwargs):
        if 'accept' in request.POST and 'export' in request.POST:
            messages.add_message(self.request, messages.ERROR, self.multi_submit_error)
        else:
            if 'accept' in request.POST:
                self.object_list = self.get_queryset()
                selected_users = request.POST.getlist('first')
                if self.training.limitless:
                    for pk in selected_users:
                        try:
                            user_training = UserTraining.objects.get(pk=pk)
                            if user_training.first_selection == self.training:
                                user_training.accepted_training = True
                                user_training.save()
                                self.accepted_count += 1
                        except UserTraining.DoesNotExist:
                            pass
                elif self.accepted_count + len(selected_users) > self.training.capacity:
                    messages.add_message(self.request, messages.ERROR, self.accepted_count_error_message)
                else:
                    for pk in selected_users:
                        try:
                            user_training = UserTraining.objects.get(pk=pk)
                            if user_training.first_selection == self.training:
                                user_training.accepted_training = True
                                user_training.save()
                                self.accepted_count += 1
                        except UserTraining.DoesNotExist:
                            pass
            if 'export' in request.POST:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="instructor.csv"'
                response.write(codecs.BOM_UTF8)
                writer = csv.writer(response)

                user_training_list = UserTraining.objects.filter(first_selection=self.training, accepted_training=True)
                for user_training in user_training_list:
                    writer.writerow([user_training.user.get_full_name(),
                                     user_training.user.email,
                                     user_training.user.institution,
                                     user_training.user.phone_number])
                return response

        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


class ParticipantTrainingAcceptedListView(LoginRequiredMixin, InfoRequiredMixin, InstructorRequiredMixin,
                                          PaginationMixin, ListView):
    model = UserTraining
    paginate_by = 50
    template_name = 'pages/profile/instructor/training_accepted_participants.html'
    training = None

    def dispatch(self, request, *args, **kwargs):
        self.get_training_object()
        self.accepted_count = UserTraining.objects.filter(first_selection=self.training).count()
        return super(ParticipantTrainingAcceptedListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParticipantTrainingAcceptedListView, self).get_context_data(**kwargs)
        context["training"] = self.training
        return context

    def get_training_object(self):
        try:
            self.training = Training.objects.get(instructor=self.request.user.instructor, pk=self.kwargs['pk'])
        except Training.DoesNotExist:
            raise Http404

    def get_queryset(self):
        term = self.request.GET.get('search', None)
        query = UserTraining.objects.filter(first_selection=self.training)
        if term:
            query = query.filter(Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term))
        return query.order_by('accepted_training')

    def post(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="instructor.csv"'
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)

        user_training_list = UserTraining.objects.filter(first_selection=self.training)
        for user_training in user_training_list:
            writer.writerow([user_training.user.get_full_name(),
                             user_training.user.email,
                             user_training.user.institution,
                             user_training.user.phone_number])
        return response


class LoginErrorView(TemplateView):
    template_name = 'pages/profile/login_error.html'


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse_lazy('hacktrick:index'))
