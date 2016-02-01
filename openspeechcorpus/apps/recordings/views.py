from django.shortcuts import render
from django.views import generic
from django.core import paginator

from openspeechcorpus.apps.tales import models as tales_models
from openspeechcorpus.apps.core import models as core_models

# Create your views here.
class RecordingsList(generic.ListView):
    template_name = "recordings/recordings/recordings_list.html"
    context_object_name = "recordings"
    queryset = core_models.AnonymousAudioData.objects.all().order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(RecordingsList, self).get_context_data(**kwargs)
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

class RecordingDetail(generic.DetailView):
    model = core_models.AudioData
    context_object_name = "recording"
    template_name = "recordings/recordings/recordings_detail.html"

    def get_context_data(self, **kwargs):
        context = super(RecordingDetail, self).get_context_data(**kwargs)

        try:
            tale_sentence_speech = tales_models.SentenceTaleSpeech.objects.get(audio=context['recording'])
            context['tale'] = tale_sentence_speech.tale_sentence.tale

        except tales_models.SentenceTaleSpeech.DoesNotExist:
            pass

        return context
