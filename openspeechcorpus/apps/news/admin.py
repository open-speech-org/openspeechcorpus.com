from django.contrib import admin

from . import models as news_models
# Register your models here.

admin.site.register(news_models.New)

