from django.contrib import admin


from . import models
# Register your models here.

admin.site.register(models.Level)
admin.site.register(models.LevelCategory)
admin.site.register(models.LevelSentence)
admin.site.register(models.LevelSentenceSpeech)
