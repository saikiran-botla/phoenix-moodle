# Generated by Django 3.2.8 on 2021-10-22 16:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moodle', '0003_auto_20211022_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coursescreated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('coursecode', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(message='Length has to be 5', regex='^\\w{5}$')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moodle.coursescreated'),
        ),
        migrations.DeleteModel(
            name='course',
        ),
    ]
