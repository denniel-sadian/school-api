# Generated by Django 3.0.5 on 2020-05-12 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('information', '0010_auto_20200512_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
