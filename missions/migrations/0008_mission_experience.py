# Generated by Django 3.2.2 on 2022-06-05 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0007_auto_20220503_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='experience',
            field=models.IntegerField(default=0, verbose_name='XP'),
        ),
    ]
