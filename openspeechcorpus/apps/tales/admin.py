from django.contrib import admin

from . import models as tales_models
# Register your models here.
admin.site.register(tales_models.Author)
admin.site.register(tales_models.Tale)
admin.site.register(tales_models.TaleSentence)
admin.site.register(tales_models.SentenceTaleSpeech)
admin.site.register(tales_models.TaleVote)
