from django.contrib import admin

from models import Exam
from models import Item
from models import Choice
from models import Session

admin.site.register(Exam)
admin.site.register(Item)
admin.site.register(Choice)
admin.site.register(Session)
