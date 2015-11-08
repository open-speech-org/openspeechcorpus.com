from django.conf.urls import url

from . import views as mobile_api_views

urlpatterns = [
    url(r'^sentences/$', mobile_api_views.TalesSentencesView.as_view(), name="mobile_api_tales_sentences"),
    url(r'^sentences/upload/', mobile_api_views.UploadTaleSetenceView.as_view(), name="mobile_api_tales_sentences_upload"),
]