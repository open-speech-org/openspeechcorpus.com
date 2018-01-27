from django.shortcuts import render
from django.views import generic
from django.core import paginator

from applications.authentication import models as authentication_models
from applications.core import models as core_models

# Create your views here.
class ProfileView(generic.DetailView):
    template_name = "user_profile/user_profile_detail.html"
    model = authentication_models.AnonymousUserProfile
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['recordings'] = core_models.AnonymousAudioData.objects.filter(user=context['user_profile'])
        context['total_recordings'] = context['recordings'].count()

        recordings_by_page = 50
        pager = paginator.Paginator(context['recordings'], recordings_by_page)
        page = self.request.GET.get('page', 1)
        try:
            recordings = pager.page(page)

            start_index = max(1, recordings.number-3)
            end_index = min(recordings.number+3, (len(context['recordings'])/recordings_by_page)+1)
            print(start_index, end_index, len(context['recordings']))
            context['range'] = range(start_index, end_index+1)
            context['recordings'] = recordings
        except paginator.PageNotAnInteger:
            context['recordings'] = pager.page(1)
        except paginator.EmptyPage:
            context['recordings'] = pager.page(pager.num_pages)
        return context

class UserProfileList(generic.ListView):
    template_name = "user_profile/user_profile_list.html"
    queryset = authentication_models.AnonymousUserProfile.objects.all()
    context_object_name = "user_profiles"