import logging

from django.http.response import Http404
from django.views.generic.base import TemplateView
from django.db.models.aggregates import Count
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import (
    Setting,
    Sponsor,
    Speaker,
    ConferenceSlot,
    Speak,
    FAQ,
    Training
)
from profiles.models import Instructor

log = logging.getLogger(__name__)
# log.error("log example", extra=self.request.log_extra)


class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["setting"] = Setting.objects.first()
        context["platinum_sponsors"] = Sponsor.objects.filter(category=0).order_by('order')
        context["gold_sponsors"] = Sponsor.objects.filter(category=1).order_by('order')
        context["silver_sponsors"] = Sponsor.objects.filter(category=2).order_by('order')
        context["supporter"] = Sponsor.objects.filter(category=3).order_by('order')
        context["media_sponsors"] = Sponsor.objects.filter(category=4).order_by('order')
        context["media_sponsors"] = Sponsor.objects.filter(category=4).order_by('order')
        context["bronze_sponsors"] = Sponsor.objects.filter(category=5).order_by('order')
        context["stand_sponsors"] = Sponsor.objects.filter(category=6).order_by('order')
        context["speakers"] = Speaker.objects.all()
        context["instructors"] = Instructor.objects.all()
        context['conference_slots'] = ConferenceSlot.objects.all()
        context['speaking_count'] = Speak.objects.all().count()
        return context


class FAQListView(ListView):
    template_name = 'pages/hacktrick/faq.html'
    model = FAQ
    ordering = 'order'


class TrainingListView(ListView):
    template_name = 'pages/hacktrick/trainings.html'
    model = Training

    def get_queryset(self):
        return Training.objects.filter(status=True)


class TrainingDetailView(DetailView):
    template_name = 'pages/hacktrick/training_detail.html'
    model = Training

    def get_context_data(self, **kwargs):
        context = super(TrainingDetailView, self).get_context_data(**kwargs)
        try:
            context["training_note"] = Setting.objects.get().training_note
        except Setting.DoesNotExist:
            context["training_note"] = ""
        context['trainings'] = Training.objects.all()
        return context

    def get_object(self, queryset=None):
        try:
            return Training.objects.get(status=True, pk=self.kwargs['pk'])
        except:
            raise Http404
