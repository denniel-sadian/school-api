# Generated by Django 3.0.5 on 2020-05-09 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_auto_20200506_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
