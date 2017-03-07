from django.conf.urls import url

from .views import (
    LoginView,
    ProfileView,
    InstructorView,
    TicketListView,
    TicketDetailView,
    user_logout
)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^instructor/$', InstructorView.as_view(), name='instructor'),
    url(r'^tickets/$', TicketListView.as_view(), name='tickets'),
    url(r'^tickets/(?P<pk>[0-9]+)$', TicketDetailView.as_view(), name='ticket_detail'),
]
