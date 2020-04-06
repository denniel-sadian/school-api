from django.db import models
from django.contrib.auth.models import User

from information.models import Department


class Employee(models.Model):
    ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.CharField(max_length=7, choices=ROLES)
    photo = models.ImageField()
