# Generated by Django 3.2.8 on 2021-11-27 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0023_alter_assignment_csvfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='weightage',
            field=models.PositiveIntegerField(null=True),
        ),
    ]