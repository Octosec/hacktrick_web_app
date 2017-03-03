from django.conf.urls import url

from .views import LoginView, ProfileView, InstructorView, user_logout

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^instructor/$', InstructorView.as_view(), name='instructor'),
]
