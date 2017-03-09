from django.conf.urls import url

from .views import IndexView, FAQListView, TrainingListView, TrainingDetailView

urlpatterns = [
    url('^$', IndexView.as_view(), name='index'),
    url('^faq/$', FAQListView.as_view(), name='faq'),
    url('^trainings/$', TrainingListView.as_view(), name='trainings'),
    url(r'^trainings/(?P<pk>[0-9]+)$', TrainingDetailView.as_view(), name='training_detail'),

]
