# Generated by Django 3.2.8 on 2021-11-27 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0021_alter_coursescreated_dis_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='csvfile',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]