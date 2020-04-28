from django.contrib import admin

from . import models


class WorkInline(admin.StackedInline):
    model = models.Work
    extra = 0


class GradingSheetAdmin(admin.ModelAdmin):
    list_display = ('date', 'teacher', 'department', 'subject', 'publish')
    inlines = [WorkInline]


class WorkAdmin(admin.ModelAdmin):
    list_display = ('date', 'gsheet', 'work_type', 'highest_score')


admin.site.register(models.GradingSheet, GradingSheetAdmin)
admin.site.register(models.Work, WorkAdmin)
admin.site.register(models.Record)
admin.site.register(models.Card)
admin.site.register(models.FinalGrade)
admin.site.register(models.ViewingPermission)
