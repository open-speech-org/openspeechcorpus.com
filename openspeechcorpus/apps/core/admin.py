from django.contrib import admin

from . import models as core_models
# Register your models here.
admin.site.register(core_models.AudioData)
admin.site.register(core_models.AnonymousAudioData)
