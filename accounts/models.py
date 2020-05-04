from django.db import models
from django_resized import ResizedImageField

from information.models import Department


class Profile(models.Model):
    ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher')
    )
    GENDERS = (
        ('m', 'Male'),
        ('f', 'Female')
    )
    user = models.OneToOneField('auth.user', on_delete=models.PROTECT)
    gender = models.CharField(max_length=1, choices=GENDERS)
    id_number = models.CharField(max_length=255, null=True, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)
    role = models.CharField(max_length=7, choices=ROLES, null=True)
    photo = ResizedImageField(size=[400, 400], upload_to='pics/', force_format='PNG', null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class ProfileUserCreationPermission(models.Model):
    from_who = models.ForeignKey('auth.user', on_delete=models.CASCADE,
                                 related_name='permissions')
    date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=7, choices=Profile.ROLES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=Profile.GENDERS)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True)
    used = models.BooleanField(default=False)

    def save(self, **kwargs):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        super().save(**kwargs)
