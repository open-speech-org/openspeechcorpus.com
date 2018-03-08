from django.conf.urls import url

from . import views as webapp_view

urlpatterns = [
    url(
        r'^authors/$',
        webapp_view.AuthorsList.as_view(),
        name="author_list"
    ),
    url(
        r'^tales/(?P<author_id>[\w]+)/$',
        webapp_view.TalesListByAuthor.as_view(),
        name="tales_by_author_list"
    ),
    url(
        r'^app/(?P<tale_id>[\w]+)/$',
        webapp_view.App.as_view(),
        name="app"
    ),
]
