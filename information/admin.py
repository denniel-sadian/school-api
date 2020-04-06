from django.contrib import admin

from . import models

admin.site.register(models.Department)
admin.site.register(models.Section)
admin.site.register(models.Subject)
admin.site.register(models.GuardianViewingPermission)
admin.site.register(models.GradingSheet)
admin.site.register(models.Student)
