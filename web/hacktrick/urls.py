from django.conf.urls import url

from .views import (
    IndexView,
    FAQListView,
    BugMinerView,
    DemoRoomView,
    GameOfPwnersView,
    CsAwardView,
    TrainingListView,
    TrainingDetailView,
    ContactView,
    AccommodationView,
    TransportationView,
    CFPView,
    ContributorListView,
    LiveBroadCastView
)

urlpatterns = [
    url('^$', IndexView.as_view(), name='index'),
    url('^faq/$', FAQListView.as_view(), name='faq'),
    url('^contact/$', ContactView.as_view(), name='contact'),
    url('^accommodation/$', AccommodationView.as_view(), name='accommodation'),
    url('^transportation/$', TransportationView.as_view(), name='transportation'),
    url(r'^events/cfp/$',CFPView.as_view(),name='cfp'),
    url(r'^events/game-of-pwners/$',GameOfPwnersView.as_view(),name='game-of-pwners'),
    url(r'^events/bugminer/$',BugMinerView.as_view(),name='bug-miner'),
    url(r'^events/demo-room/$',DemoRoomView.as_view(),name='demo-room'),
    url(r'^events/cs-awards/$',CsAwardView.as_view(),name='cs-award'),
    url(r'^trainings/$', TrainingListView.as_view(), name='trainings'),
    url(r'^trainings/(?P<pk>[0-9]{1,10})$', TrainingDetailView.as_view(), name='training_detail'),
    url(r'^contributors/$', ContributorListView.as_view(), name='contributors'),
    url(r'^live/$', LiveBroadCastView.as_view(), name='broadcast'),
]
