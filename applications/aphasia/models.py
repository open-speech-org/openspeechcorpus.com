from django.db import models

from applications.core.models import AudioData

# Create your models here.


class Level(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class LevelCategory(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    title = models.TextField()

    def __str__(self):
        return self.title


class LevelSentence(models.Model):
    level_category = models.ForeignKey(LevelCategory, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.level_category, self.text)


class LevelSentenceSpeech(models.Model):
    level_sentence = models.ForeignKey(LevelSentence, on_delete=models.CASCADE)
    audio = models.ForeignKey(AudioData, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.level_sentence) + " " + str(self.audio)
