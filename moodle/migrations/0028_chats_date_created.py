# Generated by Django 3.2.8 on 2021-11-28 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0027_remove_assignment_histogram'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
