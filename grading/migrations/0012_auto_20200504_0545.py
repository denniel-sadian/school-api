# Generated by Django 3.0.5 on 2020-05-04 05:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grading', '0011_auto_20200428_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradingsheet',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grading_sheets', to=settings.AUTH_USER_MODEL),
        ),
    ]
