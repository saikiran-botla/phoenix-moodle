# Generated by Django 3.2.8 on 2021-11-27 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0018_chats'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursescreated',
            name='dis_status',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
