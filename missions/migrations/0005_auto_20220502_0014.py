# Generated by Django 3.2.2 on 2022-05-01 22:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0004_auto_20220502_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='missionclass',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='missionclass',
            name='start_date',
        ),
        migrations.AddField(
            model_name='missionclass',
            name='end',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='end'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='missionclass',
            name='start',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='start'),
            preserve_default=False,
        ),
    ]