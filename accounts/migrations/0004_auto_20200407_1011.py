# Generated by Django 3.0.5 on 2020-04-07 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200407_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileusercreationinvitation',
            name='id',
        ),
        migrations.AlterField(
            model_name='profileusercreationinvitation',
            name='code',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
