# Generated by Django 3.2.8 on 2021-11-27 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0024_assignment_weightage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='weightage',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]