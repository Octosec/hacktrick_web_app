from django.conf.urls import url

from .views import IndexView, FAQListView

urlpatterns = [
    url('^$', IndexView.as_view(), name='index'),
    url('^faq/$', FAQListView.as_view(), name='faq'),
]
