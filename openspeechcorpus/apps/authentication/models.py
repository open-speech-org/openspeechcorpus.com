from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_token = models.CharField(max_length=40, blank=True)
    expiration = models.DateTimeField(blank=True, null=True)
    role = models.ForeignKey(Role)

    def __unicode__(self):
        return unicode(self.user)


class Permission(models.Model):
    role = models.ManyToManyField(Role)
    short_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    reverse_lazy_url = models.CharField(max_length=150)

    def __unicode__(self):
        return self.nombre


# Custom authentication

class AnonymousUserProfile(models.Model):
    anonymous_name = models.CharField(max_length=100)
    anonymous_picture = models.ImageField(upload_to='anonymous_pictures', blank=True, null=True)

    def __unicode__(self):
        return self.anonymous_name


class AnonymousUserProfileHistory(models.Model):
    anonymous_user_profile = models.ForeignKey(AnonymousUserProfile)
    anonymous_name = models.CharField(max_length=100, blank=True, null=True)
    anonymous_picture = models.ImageField(upload_to='anonymous_pictures', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.timestamp) + " " + unicode(self.anonymous_user_profile)