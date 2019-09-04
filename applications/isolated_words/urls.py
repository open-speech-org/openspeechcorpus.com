from django.conf.urls import url

from . import (
    views,
    conf
)

urlpatterns = [
    url(
        '^list/$',
        views.List.as_view(),
        name=conf.ISOLATED_WORD_SPEECH_LIST_URL_NAME
    )
]
