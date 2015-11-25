from django.shortcuts import render
from django.views import generic

from openspeechcorpus.apps.authentication import models as authentication_models
from openspeechcorpus.apps.core import models as core_models

# Create your views here.
class ProfileView(generic.DetailView):
    template_name = "user_profile/user_profile_detail.html"
    model = authentication_models.AnonymousUserProfile
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['recordings'] = core_models.AnonymousAudioData.objects.filter(user=context['user_profile'])
        return context

class UserProfileList(generic.ListView):
    template_name = "user_profile/user_profile_list.html"
    queryset = authentication_models.AnonymousUserProfile.objects.all()
    context_object_name = "user_profiles"