from django.conf.urls import url

from . import views as recordings_views
urlpatterns = [
    url(r'^list/$', recordings_views.RecordingsList.as_view(), name='recordings_list'),
    url(r'^detail/(?P<slug>[\w-]+)/$', recordings_views.RecordingDetail.as_view(), name='recording_view'),
]