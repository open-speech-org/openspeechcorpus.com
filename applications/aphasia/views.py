from django.shortcuts import render

from django.views import generic
from django.core import paginator
from django.db.models import Count

from . import models
from applications.authentication import models as authentication_models
# Create your views here.


class List(generic.ListView):
    template_name = "aphasia/list.html"
    context_object_name = "recordings"
    queryset = models.LevelSentenceSpeech.objects.all().order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        recordings_by_page = 50
        context['total_recordings'] = context['recordings'].count()
        pager = paginator.Paginator(context['recordings'], recordings_by_page)
        page = self.request.GET.get('page', 1)
        try:
            recordings = pager.page(page)

            start_index = max(1, recordings.number-3)
            end_index = min(recordings.number+3, (len(context['recordings'])//recordings_by_page)+1)
            print(start_index, end_index, len(context['recordings']))
            context['range'] = range(start_index, end_index+1)
            context['recordings'] = recordings
        except paginator.PageNotAnInteger:
            context['recordings'] = pager.page(1)
        except paginator.EmptyPage:
            context['recordings'] = pager.page(pager.num_pages)

        return context


class SortedByContributors(generic.TemplateView):
    template_name = 'static_html/index.html'

    def get_context_data(self, **kwargs):
        context = super(SortedByContributors, self).get_context_data()

        count_datas = models.LevelSentenceSpeech.objects.values('audio__anonymousaudiodata__user').annotate(
            user_count=Count('audio__anonymousaudiodata__user')
        ).order_by('-user_count')
        print(count_datas)

        for count_data in count_datas:
            count_data['audio__anonymousaudiodata__user'] = authentication_models.AnonymousUserProfile.objects.get(
                pk=count_data['audio__anonymousaudiodata__user']
            ) if count_data['audio__anonymousaudiodata__user'] else None

        context['ranking'] = count_datas

        return context
