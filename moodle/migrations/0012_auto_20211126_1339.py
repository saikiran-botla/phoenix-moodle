# Generated by Django 3.2.8 on 2021-11-26 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0011_alter_ta_edit_privileges'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ta',
            name='edit_privileges',
        ),
        migrations.AddField(
            model_name='ta',
            name='create_assignment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ta',
            name='enroll_student',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ta',
            name='givefeedback',
            field=models.BooleanField(default=True),
        ),
    ]