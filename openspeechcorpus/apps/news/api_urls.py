from django.conf.urls import url

from . import api_views as news_api_views

urlpatterns = [
    url(
        r'^all/$',
        news_api_views.AllNews.as_view(),
        name="all")
]