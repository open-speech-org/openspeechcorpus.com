from django.db import models
from openspeechcorpus.apps.core.models import AudioData
# Create your models here.
class Tale(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(Author)


class TaleSentence(models.Model):
    tale = models.ForeignKey(Tale)
    place = models.IntegerField(blank=True, null=True)
    text = models.TextField()


class SentenceTaleSpeech(models.Model):
    tale_sentence = models.ForeignKey(TaleSentence)
    audio = models.ForeignKey(AudioData)


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    death = models.DateField(blank=True, null=True)
    styles = models.ManyToManyField(Style)


class Style(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    starts = models.DateField(blank=True, null=True)
    ends = models.DateField(blank=True, null=True)

