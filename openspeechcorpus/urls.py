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
from django.urls import include, path
from django.contrib import admin
from django.views.static import serve as django_static_serve

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.static_html.urls')),
    path('auth/', include('applications.authentication.urls')),
    path('api/', include('applications.mobile_api.urls')),
    path('recordings/', include('applications.recordings.urls')),
    path('contributors/', include('applications.user_profile.urls')),
    path('webapp/', include('applications.webapp.urls')),
    path('aphasia/', include('applications.aphasia.urls')),


    # Media URL
    path(
        '^media/(?P<path>.*)$',
        django_static_serve,
        {
            'document_root': settings.MEDIA_ROOT
        }
    ),
]
