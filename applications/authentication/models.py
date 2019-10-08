from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_token = models.CharField(max_length=40, blank=True)
    expiration = models.DateTimeField(blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Permission(models.Model):
    role = models.ManyToManyField(Role)
    short_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    reverse_lazy_url = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre


# Custom authentication

class AnonymousUserProfile(models.Model):
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male')
    )
    anonymous_name = models.CharField(max_length=100)
    anonymous_picture = models.ImageField(upload_to='anonymous_pictures', blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        default=''
    )
    age = models.PositiveIntegerField(default=1)
    accent = models.TextField(default="", blank=True)
    pitch = models.TextField(default="", blank=True)
    height = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "{} {}".format(str(self.id), self.anonymous_name)


class AnonymousUserProfileHistory(models.Model):
    anonymous_user_profile = models.ForeignKey(AnonymousUserProfile, on_delete=models.CASCADE)
    anonymous_name = models.CharField(max_length=100, blank=True, null=True)
    anonymous_picture = models.ImageField(upload_to='anonymous_pictures', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.timestamp) + " " + str(self.anonymous_user_profile)