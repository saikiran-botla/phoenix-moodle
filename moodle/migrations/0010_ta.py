# Generated by Django 3.2.8 on 2021-11-26 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moodle', '0009_alter_assignment_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edit_privileges', models.CharField(choices=[('basic', 'basic'), ('instructor level', 'instructor level')], max_length=200, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moodle.coursescreated')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
