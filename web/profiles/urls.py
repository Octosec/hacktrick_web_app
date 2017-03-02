from django.conf.urls import url

from .views import LoginView, ProfileView, user_logout

urlpatterns = [
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', user_logout, name='logout'),
    url('^profile/$', ProfileView.as_view(), name='profile'),
]
