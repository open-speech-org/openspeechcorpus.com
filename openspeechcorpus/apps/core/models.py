from django.db import models
from django.contrib.auth.models import User

from openspeechcorpus.apps.authentication.models import AnonymousUserProfile

# Create your models here.
class AudioData(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    text = models.TextField()
    audiofile = models.FileField(upload_to='audio-data')
    user = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    frecuency = models.CharField(max_length=12, blank=True, null=True)
    channels = models.CharField(max_length=2, blank=True, null=True)

    def __unicode__(self):
        return self.name


class AnonymousAudioData(models.Model):
    audio = models.ForeignKey(AudioData)
    user = models.ForeignKey(AnonymousUserProfile)

    def __unicode__(self):
        return unicode(self.user) + ": " +unicode(self.audio)