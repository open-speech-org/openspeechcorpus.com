from django.db import models
from django.contrib.auth.models import User

from applications.authentication import models as authentication_models
# Create your models here.


class Suggestion(models.Model):
    suggestion = models.TextField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    anonymous_user = models.ForeignKey(authentication_models.AnonymousUserProfile, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.suggestion
