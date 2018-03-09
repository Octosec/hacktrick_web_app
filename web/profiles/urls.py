from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test

from .views import (
    LoginView,
    ProfileView,
    InstructorView,
    TicketListView,
    TicketDetailView,
    TrainingListView,
    TrainingUpdateView,
    TrainingDocumentListView,
    TrainingDocumentDeleteView,
    ParticipantSelectTrainingView,
    InstructorAcceptParticipantView,
    ParticipantTrainingAcceptedListView,
    LoginErrorView,
    user_logout
)

login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = [
    url(r'^login/$', login_forbidden(LoginView.as_view()), name='login'),
    url(r'^login/error/$', LoginErrorView.as_view(), name='login_error'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^instructor/$', InstructorView.as_view(), name='instructor'),
    url(r'^tickets/$', TicketListView.as_view(), name='tickets'),
    url(r'^tickets/(?P<pk>[0-9]{1,10})$', TicketDetailView.as_view(), name='ticket_detail'),

    url(r'^participant/trainings/select/$', ParticipantSelectTrainingView.as_view(), name='training_select'),
    url(r'^instructor/trainings/$', TrainingListView.as_view(), name='trainings'),
    url(r'^instructor/trainings/(?P<pk>[0-9]{1,10})$', TrainingUpdateView.as_view(), name='training_update'),
    url(r'^instructor/trainings/(?P<pk>[0-9]{1,10})/documents/$',
        TrainingDocumentListView.as_view(),
        name='training_documents'),
    url(r'^instructor/trainings/documents/delete/(?P<pk>[0-9]{1,10})$',
        TrainingDocumentDeleteView.as_view(),
        name='delete_documents'),
    url(r'^instructor/trainings/(?P<pk>[0-9]{1,10})/accept/$',
        InstructorAcceptParticipantView.as_view(),
        name='participant_accept'),
    url(r'^instructor/trainings/(?P<pk>[0-9]{1,10})/participants/accepted/$',
        ParticipantTrainingAcceptedListView.as_view(),
        name='accepted_participants'),
]
