from django.conf.urls import url

from . import views as mobile_api_views

urlpatterns = [
    url(
        r'^sentences/$',
        mobile_api_views.TalesSentencesView.as_view(),
        name="mobile_api_tales_sentences"
    ),
    url(
        r'^sentences/upload/',
        mobile_api_views.UploadTaleSetenceView.as_view(),
        name="mobile_api_tales_sentences_upload"
    ),
    url(
        r'^suggestion/upload/',
        mobile_api_views.RegisterSuggestion.as_view(),
        name="mobile_api_tales_suggestion_upload"
    ),
    url(
        r'^anonymous-user/update/',
        mobile_api_views.UpdateAnonymousUserProfile.as_view(),
        name="mobile_api_anonymous_user_profile_update"
    ),
    url(
        r'^custom/upload/',
        mobile_api_views.UploadCustomAudio.as_view(),
        name="mobile_api_custom_upload"
    ),
]