# Generated by Django 3.2.8 on 2021-11-27 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0020_alter_coursescreated_dis_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursescreated',
            name='dis_status',
            field=models.BooleanField(default=True),
        ),
    ]
