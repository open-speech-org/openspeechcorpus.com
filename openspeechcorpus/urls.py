"""openspeechcorpus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from openspeechcorpus.apps.static_html import urls as static_html_urls
from openspeechcorpus.apps.authentication import urls as authentication_urls
from openspeechcorpus.apps.mobile_api import urls as mobile_api_urls
from openspeechcorpus.apps.recordings import urls as recordings_urls
from openspeechcorpus.apps.user_profile import urls as user_profiles_urls
from . import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(static_html_urls)),
    url(r'^auth/', include(authentication_urls)),
    url(r'^api/', include(mobile_api_urls)),
    url(r'^recordings/', include(recordings_urls)),
    url(r'^contributors/', include(user_profiles_urls)),

    # Media URL
    url(
        r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {
            'document_root': settings.MEDIA_ROOT
        }
    ),
]
