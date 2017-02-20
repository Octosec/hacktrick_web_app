from django.conf.urls import url, include


urlpatterns = [
    url(r'^auth/', include('api.auth.urls', namespace="auth")),
]
