from django.db import models

# Create your models here.
class New(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __unicode__(self):
        return self.title