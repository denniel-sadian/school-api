from django.db import models
from django.contrib.auth.models import User


class ModelWithNameOnly(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    
    def save(self, **kwargs):
        self.name = self.name.upper()
        super().save(**kwargs)


class Department(ModelWithNameOnly):
    pass


class Section(ModelWithNameOnly):
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='sections')


class Subject(ModelWithNameOnly):
    pass


class GuardianViewingPermission(models.Model):
    from_who = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)

    class Meta:
        unique_together = ('code', 'section')

    def __str__(self):
        return self.code


class Student(models.Model):
    LEVELS = (
        ('1', 'Grade 1'),
        ('2', 'Grade 2'),
        ('3', 'Grade 3'),
        ('4', 'Grade 4'),
        ('5', 'Grade 5'),
        ('6', 'Grade 6'),
        ('7', 'Grade 7'),
        ('8', 'Grade 8'),
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
        ('c1', 'First Year College'),
        ('c2', 'Second Year College'),
        ('c3', 'Third Year College'),
        ('c4', 'Fourth Year College')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=100, unique=True)
    cp_number = models.CharField(max_length=12)
    guardian_cp_number = models.CharField(max_length=12)
    address = models.CharField(max_length=255)
    photo = models.ImageField(null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    grade_level = models.CharField(max_length=2, choices=LEVELS)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, **kwargs):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        self.address = self.address.upper()
        super().save(**kwargs)
