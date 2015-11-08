from django.shortcuts import render
from django.views import generic

from openspeechcorpus.apps.tales import models as tales_models
from openspeechcorpus.apps.core import models as core_models

# Create your views here.
class RecordingsList(generic.ListView):
    template_name = "recordings/recordings/recordings_list.html"
    context_object_name = "recordings"
    queryset = core_models.AudioData.objects.all()


class RecordingDetail(generic.DetailView):
    model = core_models.AudioData
    context_object_name = "recording"
    template_name = "recordings/recordings/recordings_detail.html"