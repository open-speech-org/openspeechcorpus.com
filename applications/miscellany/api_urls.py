from django.conf.urls import url

from . import api_views as miscellany_api_views

urlpatterns = [
    url(
        r'^list/$',
        miscellany_api_views.CommandsView.as_view(),
        name="list"
    ),
    url(
        r'^upload/$',
        miscellany_api_views.UploadCommand.as_view(),
        name="upload"
    ),
]