from django.conf.urls import url

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
    user_logout
)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^instructor/$', InstructorView.as_view(), name='instructor'),
    url(r'^tickets/$', TicketListView.as_view(), name='tickets'),
    url(r'^tickets/(?P<pk>[0-9]+)$', TicketDetailView.as_view(), name='ticket_detail'),
    url(r'^trainings/$', TrainingListView.as_view(), name='trainings'),
    url(r'^trainings/(?P<pk>[0-9]+)$', TrainingUpdateView.as_view(), name='training_update'),
    url(r'^trainings/(?P<pk>[0-9]+)/documents/$', TrainingDocumentListView.as_view(), name='training_documents'),
    url(r'^trainings/documents/delete/(?P<pk>[0-9]+)$', TrainingDocumentDeleteView.as_view(), name='delete_documents')
]
