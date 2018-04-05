from django.conf.urls import url, include

from . import (
    views as mobile_api_views,
    conf as mobile_api_conf
)
from applications.news import api_urls as news_api_urls
from applications.miscellany import api_urls as miscellany_api_urls

urlpatterns = [
    url(
        r'^sentences/$',
        mobile_api_views.TalesSentencesView.as_view(),
        name="mobile_api_tales_sentences"
    ),
    url(
        r'^sentences/random/$',
        mobile_api_views.GetRandomSentence.as_view(),
        name="mobile_api_get_random_tale_sentence"
    ),
    url(
        r'^sentences/next/$',
        mobile_api_views.GetNextSentence.as_view(),
        name="mobile_api_get_next_tale_sentence"
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
    url(
        r'^tales/$',
        mobile_api_views.GetTales.as_view(),
        name="mobile_api_tales"
    ),
    url(
        r'^tales/rate/$',
        mobile_api_views.VoteTale.as_view(),
        name="mobile_api_vote_tale"
    ),
    url(
        r'^authors/',
        mobile_api_views.GetAuthors.as_view(),
        name="mobile_api_authors"
    ),
    url(

        r'^tales/(?P<author_id>[\w]+)/$',
        mobile_api_views.GetTalesOfAuthor.as_view(),
        name="mobile_api_tales_of_author"
    ),
    url(

        r'^sentences/(?P<tale_id>[\w]+)/$',
        mobile_api_views.GetSentencesOfTale.as_view(),
        name="mobile_api_sentences_of_tale"
    ),
    url(
        r'^news/',
        include(news_api_urls)
    ),
    url(
        r'^commands/',
        include(miscellany_api_urls)
    ),
    url(
        r'ranking/',
        mobile_api_views.RankingTable.as_view(),
        name="mobile_api_ranking_table"
    ),
    url(
        r'most_readed_sentence_speech/',
        mobile_api_views.DownloadMostReadedTales.as_view(),
        name="mobile_api_most_readed_sencente_speech"
    ),

    # #### APHASIA #####
    url(
        r'^levels/$',
        mobile_api_views.GetLevels.as_view(),
        name=mobile_api_conf.APHASIA_LEVELS_URL_NAME
    ),
    url(
        r'^level/(?P<pk_level>\d+)/$',
        mobile_api_views.GetLevelCategory.as_view(),
        name=mobile_api_conf.APHASIA_LEVEL_CATEGORY_URL_NAME
    ),
    url(
        r'^level/(?P<pk_level>\d+)/category/(?P<pk_level_category>\d+)$',
        mobile_api_views.GetLevelSentence.as_view(),
        name=mobile_api_conf.APHASIA_LEVEL_CATEGORY_SENTENCES_URL_NAME
    ),
    url(
        r'^words/upload/$',
        mobile_api_views.UploadLevelSentence.as_view(),
        name=mobile_api_conf.APHASIA_UPLOAD_LEVEL_SENTENCE_URL_NAME
    )

]
