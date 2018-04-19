from datetime import timedelta

from django.shortcuts import render
from django.views import generic
from django.db import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core import paginator
from django.utils.datetime_safe import datetime
from django.utils import timezone
from itertools import chain

from applications.core import models as core_models
from applications.authentication import models as authentication_models
from applications.tales import models as tales_models

# Create your views here.


class Index(generic.TemplateView):
    template_name = 'static_html/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data()

        count_datas = core_models.AnonymousAudioData.objects.values('user').annotate(
            user_count=models.Count('user')
        ).order_by('-user_count')

        for count_data in count_datas:
            count_data['user'] = authentication_models.AnonymousUserProfile.objects.get(pk=count_data['user'])

        context['ranking'] = count_datas

        return context


class Donate(generic.TemplateView):
    template_name = 'static_html/donate.html'


class Download(generic.TemplateView):
    template_name = 'static_html/download.html'


class Learn(generic.TemplateView):
    template_name = 'static_html/learn.html'


class Listen(generic.TemplateView):
    template_name = 'static_html/listen.html'


class RateList(generic.ListView):
    template_name = "static_html/rate_list.html"
    context_object_name = "recordings"
    queryset = core_models.AudioData.objects.filter(verified=False)

    def get_context_data(self, **kwargs):
        context = super(RateList, self).get_context_data(**kwargs)
        recordings_by_page = 50
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


class Rate(generic.UpdateView):
    template_name = 'static_html/rate.html'
    model = core_models.AudioData
    fields = (
        'text',
    )
    context_object_name = "audio_data"

    @method_decorator(login_required(login_url=reverse_lazy('log-in')))
    def dispatch(self, request, *args, **kwargs):
        return super(Rate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(Rate, self).get_context_data(**kwargs)
        old_text = core_models.AudioData.objects.get(pk=self.kwargs['pk']).text
        context['next_id'] = core_models.AudioData.objects.filter(verified=False).filter(pk__gt=self.kwargs['pk'])[0].id
        if self.request.POST:
            context['old_text'] = old_text
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        audio_data = form.save(commit=False)
        print(form.cleaned_data['text'])
        print(context['audio_data'].text)
        print(audio_data.text)
        verification_history = core_models.VerificationHistory(
            audio_data=audio_data,
            user=self.request.user,
            original_text=context['old_text'],
            correct_text=audio_data.text
        )
        verification_history.save()
        # audio_data.verified = True
        audio_data.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        audio_datas = core_models.AudioData.objects.filter(verified=False).filter(pk__gt=self.kwargs['pk'])
        if len(audio_datas) > 0:
            return reverse_lazy('rate_update', kwargs={'pk':audio_datas[0].id})


class RecordingsGrowth(generic.TemplateView):
    template_name = "static_html/recordings_growth.html"

    def get_context_data(self, **kwargs):
        context = super(RecordingsGrowth, self).get_context_data(**kwargs)

        all_recordings = core_models.AudioData.objects.all().order_by('created')

        recordings_count = []
        labels = []
        datas = []
        initial_date = all_recordings[0].created
        date = initial_date
        days_to_group = self.request.GET.get("days", 7)
        while date < timezone.make_aware(datetime.today(), timezone.get_default_timezone()):
            new_date = date + timedelta(days=days_to_group)
            date_element = dict()
            date_element['date'] = new_date
            date_element['count'] = all_recordings.filter(created__range=[initial_date, new_date]).count()
            recordings_count.append(date_element)
            labels.append(date_element['date'])
            datas.append(date_element['count'])
            date = new_date

        context['recordings_count'] = recordings_count
        context['labels'] = labels
        context['datas'] = datas

        return context


class CountSentenceTales(generic.TemplateView):
    template_name = "static_html/sentence_tales_ordered.html"

    def get_context_data(self, **kwargs):
        context = super(CountSentenceTales, self).get_context_data(**kwargs)

        sentence_tales = tales_models.SentenceTaleSpeech.objects.values('tale_sentence').annotate(
            count=models.Count('tale_sentence')
        ).order_by('-count')[:100]

        for s in sentence_tales:
            print(s['tale_sentence'])
            s['tale_sentence'] = tales_models.TaleSentence.objects.get(pk=s['tale_sentence'])
            print(s['tale_sentence'])
        context['count'] = sentence_tales

        return context

