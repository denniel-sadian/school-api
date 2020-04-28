# Generated by Django 3.0.5 on 2020-04-28 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0006_delete_guardianviewingpermission'),
        ('grading', '0009_card_finalgrade'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewingPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('code', models.CharField(max_length=100)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewing_permissions', to='information.Section')),
            ],
            options={
                'unique_together': {('section', 'code')},
            },
        ),
    ]
