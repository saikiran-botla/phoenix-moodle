# Generated by Django 3.2.8 on 2021-11-27 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0015_announcements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcements',
            name='message',
            field=models.TextField(null=True),
        ),
    ]
