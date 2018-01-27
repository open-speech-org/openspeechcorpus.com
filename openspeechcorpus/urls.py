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

from . import settings

urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('applications.static_html.urls')),
    url(r'^auth/', include('applications.authentication.urls')),
    url(r'^api/', include('applications.mobile_api.urls')),
    url(r'^recordings/', include('applications.recordings.urls')),
    url(r'^contributors/', include('applications.user_profile.urls')),
    url(r'^webapp/', include('applications.webapp', namespace='webapp')),


    # Media URL
    url(
        r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {
            'document_root': settings.MEDIA_ROOT
        }
    ),
]
