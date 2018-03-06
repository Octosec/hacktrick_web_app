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
    BugMiner,
    GameOfPwners,
    DemoRoom,
    CsAward,
    Training,
    Contributor
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
        context["bronze_sponsors"] = Sponsor.objects.filter(category=5).order_by('order')
        context["stand_sponsors"] = Sponsor.objects.filter(category=6).order_by('order')
        context["speakers"] = Speaker.objects.filter(is_visible=True)
        context["instructors"] = Instructor.objects.all()
        context['conference_slots'] = ConferenceSlot.objects.all()
        context['speaking_count'] = Speak.objects.all().count()
        return context


class FAQListView(ListView):
    template_name = 'pages/hacktrick/faq.html'
    model = FAQ
    ordering = 'order'

class BugMinerView(TemplateView):
    template_name = 'pages/hacktrick/bug-miner.html'
    model = BugMiner


    def get_context_data(self, **kwargs):
        context = super(BugMinerView, self).get_context_data(**kwargs)
        try:
            context["bugminer"] = BugMiner.objects.all()
        except Exception as e:
            context['bugminer'] = e
        return context

class GameOfPwnersView(TemplateView):
    template_name = 'pages/hacktrick/game-of-pwners.html'
    model = GameOfPwners

    def get_context_data(self, **kwargs):
        context = super(GameOfPwnersView, self).get_context_data(**kwargs)
        try:
            context["gameofpwner"] = GameOfPwners.objects.all()
        except Exception as e:
            context['gameofpwner'] = e
        return context

class DemoRoomView(TemplateView):
    template_name = 'pages/hacktrick/demo-room.html'
    model = DemoRoom

    def get_context_data(self, **kwargs):
        context = super(DemoRoomView, self).get_context_data(**kwargs)
        try:
            context["demoroom"] = DemoRoom.objects.all()
        except Exception as e:
            context['demoroom'] = e
        return context

class CsAwardView(TemplateView):
    template_name = 'pages/hacktrick/cs-awards.html'
    model = CsAward

    def get_context_data(self, **kwargs):
        context = super(CsAwardView, self).get_context_data(**kwargs)
        try:
            context["csaward"] = CsAward.objects.all()
        except Exception as e:
            context['csaward'] = e
        return context

class TrainingListView(ListView):
    template_name = 'pages/hacktrick/trainings.html'
    model = Training

    def get_queryset(self):
        return Training.objects.all()


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
            return Training.objects.get(pk=self.kwargs['pk'])
        except:
            raise Http404


class CFPView(TemplateView):
    template_name = 'pages/hacktrick/cfp.html'

    def get_context_data(self, **kwargs):
        context = super(CFPView, self).get_context_data(**kwargs)
        context["setting"] = Setting.objects.first()
        return context


class ContributorListView(ListView):
    template_name = 'pages/hacktrick/contributor.html'
    model = Contributor

    def get_queryset(self):
        return Contributor.objects.filter(status=True)


class LiveBroadCastView(TemplateView):
    template_name = 'pages/hacktrick/live_broadcast.html'
    def get_context_data(self, **kwargs):
        context = super(LiveBroadCastView, self).get_context_data(**kwargs)
        try:
            broadcast = Setting.objects.first().live_broadcast
            if not broadcast:
                raise Http404
            context["broadcast"] = broadcast
        except Exception as e:
            raise Http404
        return context
