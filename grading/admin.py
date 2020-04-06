from django.contrib import admin

from . import models

admin.site.register(models.GradingSheet)
admin.site.register(models.Work)
admin.site.register(models.Record)
