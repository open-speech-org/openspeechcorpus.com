from django.db import models

from applications.core.models import AudioData
from applications.authentication.models import AnonymousUserProfile
# Create your models here.


class Style(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    starts = models.DateField(blank=True, null=True)
    ends = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    death = models.DateField(blank=True, null=True)
    styles = models.ManyToManyField(Style, blank=True, null=True)

    def __str__(self):
        return self.name


class Tale(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    total_votes = models.PositiveIntegerField(default=0)
    calification = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.title


class TaleVote(models.Model):
    calification = models.DecimalField(max_digits=3, decimal_places=2)
    opinion = models.TextField(blank=True, null=True)
    tale = models.ForeignKey(Tale, on_delete=models.CASCADE)
    anonymous_user = models.ForeignKey(AnonymousUserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('tale', 'anonymous_user'),
        )


class TaleSentence(models.Model):
    tale = models.ForeignKey(Tale, on_delete=models.CASCADE)
    place = models.IntegerField(blank=True, null=True)
    text = models.TextField()

    def __str__(self):
        return str(self.id) + " " + str(self.tale) + " " + str(self.place)


class SentenceTaleSpeech(models.Model):
    tale_sentence = models.ForeignKey(TaleSentence, on_delete=models.CASCADE)
    audio = models.ForeignKey(AudioData, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.tale_sentence) + " " + str(self.audio)




