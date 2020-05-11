from django.db import models

from grading.models import GradingSheet
from information.models import Student

CHOICES = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D')
)


class Exam(models.Model):
    teacher = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    sheets = models.ManyToManyField(GradingSheet)


class Item(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='items')
    question = models.CharField(max_length=255)
    correct = models.CharField(choices=CHOICES, max_length=1)


class Choice(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='choices')
    letter = models.CharField(choices=CHOICES, max_length=1)
    text = models.CharField(max_length=255)

    class Meta:
        unique_together = ('item', 'letter')


class Session(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sessions')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField(auto_now_add=True)


class AdminComment(models.Model):
    admin = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
