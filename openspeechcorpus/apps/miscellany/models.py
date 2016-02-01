from django.db import models

from openspeechcorpus.apps.core import models as core_models

# Create your models here.
class CommandCategory(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Command(models.Model):
    text = models.TextField()
    category = models.ManyToManyField(CommandCategory, blank=True)

    def __unicode__(self):
        return self.text


class CommandSpeech(models.Model):
    command = models.ForeignKey(Command)
    audio = models.ForeignKey(core_models.AudioData)
