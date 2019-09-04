from django.db import models

from applications.core.models import AudioData
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class IsolatedWord(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    text = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.category, self.text)


class IsolatedWordSpeech(models.Model):
    isolated_word = models.ForeignKey(IsolatedWord, on_delete=models.SET_NULL, null=True)
    audio = models.ForeignKey(AudioData, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.isolated_word) + " " + str(self.audio)
