from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    url(
        regex=r'^login/?$',
        view=obtain_auth_token,
        name="api-login"
    ),
]
