from django.contrib import admin

from . import models as authentication_models

# Register your models here.

admin.site.register(authentication_models.AnonymousUserProfile)
admin.site.register(authentication_models.AnonymousUserProfileHistory)
