# Generated by Django 3.0.5 on 2020-04-26 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grading', '0007_auto_20200421_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradingsheet',
            name='grading',
            field=models.CharField(choices=[('prelim', 'Prelim'), ('midterm', 'Midterm'), ('finals', 'Finals')], default='finals', max_length=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gradingsheet',
            name='sem',
            field=models.CharField(choices=[('1', 'First Semester'), ('2', 'Second Semester')], default=2, max_length=1),
            preserve_default=False,
        ),
    ]
