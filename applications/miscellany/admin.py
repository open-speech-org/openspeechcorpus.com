from django.contrib import admin

from . import models as miscellany_models
# Register your models here.

admin.site.register(miscellany_models.CommandCategory)
admin.site.register(miscellany_models.Command)
admin.site.register(miscellany_models.CommandSpeech)
