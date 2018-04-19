from django.conf.urls import url

from . import (
    views,
    conf
)

urlpatterns = [
    url(
        '^list/$',
        views.List.as_view(),
        name=conf.LEVELSENTENCESPEECH_LIST_URL_NAME
    )
]