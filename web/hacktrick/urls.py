from django.conf.urls import url

from .views import IndexView, FAQListView, TrainingListView, TrainingDetailView, CFPView, ContributorListView

urlpatterns = [
    url('^$', IndexView.as_view(), name='index'),
    url('^faq/$', FAQListView.as_view(), name='faq'),
    url('^cfp/$', CFPView.as_view(), name='cfp'),
    url('^trainings/$', TrainingListView.as_view(), name='trainings'),
    url(r'^trainings/(?P<pk>[0-9]{1,10})$', TrainingDetailView.as_view(), name='training_detail'),
    url(r'^contributors/$', ContributorListView.as_view(), name='contributors'),
]
