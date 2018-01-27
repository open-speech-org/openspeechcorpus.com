from django.conf.urls import url

from . import views as user_profile_views

urlpatterns = [
    url(r'^list/$', user_profile_views.UserProfileList.as_view(), name='user_profiles_list'),
    url(r'^detail/(?P<pk>[\w-]+)/$', user_profile_views.ProfileView.as_view(), name='user_profiles_detail'),
]