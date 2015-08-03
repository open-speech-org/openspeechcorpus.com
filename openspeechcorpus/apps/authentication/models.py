from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ActivationToken(models.Model):
    user = models.OneToOneField(User)
    activation_token = models.CharField(max_length=40, blank=True)
    expiration = models.DateTimeField(blank=True, null=True)


    def __unicode__(self):
        return unicode(self.user)