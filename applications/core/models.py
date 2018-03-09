from ffprobe3 import FFProbe
import boto3
import subprocess

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage

from django.conf import LazySettings

from applications.authentication.models import AnonymousUserProfile

settings = LazySettings()

# Create your models here.


class AudioData(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    text = models.TextField()
    audiofile = models.FileField(upload_to='audio-data', storage=FileSystemStorage())
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    frecuency = models.CharField(max_length=12, blank=True, null=True)
    channels = models.CharField(max_length=2, blank=True, null=True)
    verified = models.BooleanField(default=False)
    length = models.DecimalField(decimal_places=3, default=0, max_digits=9)

    def __str__(self):
        return self.name


class AnonymousAudioData(models.Model):
    audio = models.ForeignKey(AudioData, on_delete=models.CASCADE)
    user = models.ForeignKey(AnonymousUserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ": " + str(self.audio)


class VerificationHistory(models.Model):
    audio_data = models.ForeignKey(AudioData, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    original_text = models.TextField()
    correct_text = models.TextField()

    def __str__(self):
        return str(self.audio_data.id) + " " + str(self.user) + " " + str(self.audio_data)


class AudioDatasMigration(models.Model):
    old_user = models.ForeignKey(AnonymousUserProfile, related_name="old_user", on_delete=models.CASCADE)
    new_user = models.ForeignKey(AnonymousUserProfile, related_name="new_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=AudioData)
def calculate_length_and_upload_to_s3(sender, instance, **kwargs):
    post_save.disconnect(calculate_length_and_upload_to_s3, sender=sender)
    ffprobe = FFProbe(str(instance.audiofile.file.name))
    print(str(instance.audiofile.file.name))
    print(ffprobe.duration)
    if ffprobe.duration is not None:
        instance.length = ffprobe.duration
    else:
        instance.length = 0
    # try:
    #     ffprobe_out = subprocess.Popen(
    #         "ffprobe " + str(instance.audiofile.file.name),
    #         shell=True,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.STDOUT,
    #         close_fds=True
    #     )
    #     for line in ffprobe_out.stdout.readlines():
    #         line = line.decode()
    #         if "Duration" in line:
    #             values = line.split(",")[0].split("Duration:")[1].split(":")
    #             duration = 3600 * float(values[0]) + 60 * float(values[1]) + float(values[2])
    #             ffprobe_out.stdout.close()
    #             ffprobe_out()
    #             ffprobe_out.wait()
    #             print(duration)
    #             instance.length = duration
    #
    #     ffprobe_out.stdout.close()
    #     ffprobe_out.pipe_cloexec()
    # except IOError:
    #     print("0")
    #     instance.length = 0
    instance.save()
    upload_to_s3(instance)
    post_save.connect(calculate_length_and_upload_to_s3, sender=sender)


def upload_to_s3(instance):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    data = instance.audiofile.file.open()
    print(instance.audiofile.file)
    print(instance.audiofile.file.name)
    print(instance)
    print(instance.id)
    key = "{}/{}".format(settings.MEDIAFILES_LOCATION, "audio-data/v2/{}".format(instance.id))
    if "blob" in instance.audiofile.file.name:
        key += ".wav"
    else:
        key += ".mp4"
    s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
        Key=key,
        Body=data
    )
    print("Saved successfull")
    print(key)
