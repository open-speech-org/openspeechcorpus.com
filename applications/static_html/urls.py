from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^download/$', views.Download.as_view(), name='download'),
    url(r'^donate/$', views.Donate.as_view(), name='donate'),
    url(r'^rate/$', views.RateList.as_view(), name='rate'),
    url(r'^rate/(?P<pk>[\w-]+)/$', views.Rate.as_view(), name='rate_update'),
    url(r'^listen/$', views.Listen.as_view(), name='listen'),
    url(r'^learn/$', views.Learn.as_view(), name='learn'),
    url(r'^recordings_count/$', views.RecordingsGrowth.as_view(), name='recordings_count'),
    url(r'^sentences_tales_count/$', views.CountSentenceTales.as_view(), name='sentence_tales_count'),
]
