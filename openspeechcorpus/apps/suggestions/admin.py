from django.contrib import admin

from . import models as suggestions_models
# Register your models here.
admin.site.register(suggestions_models.Suggestion)
