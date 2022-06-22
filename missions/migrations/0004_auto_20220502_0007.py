# Generated by Django 3.2.2 on 2022-05-01 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('missions', '0003_auto_20220501_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='for_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='missions', to='missions.missionclass', verbose_name='for class'),
        ),
        migrations.AlterField(
            model_name='missionclass',
            name='end_date',
            field=models.DateField(verbose_name='end_date'),
        ),
        migrations.AlterField(
            model_name='missionclass',
            name='start_date',
            field=models.DateField(verbose_name='start_date'),
        ),
        migrations.AlterField(
            model_name='missionperson',
            name='on_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='missions.missionclass', verbose_name='on class'),
        ),
        migrations.AlterField(
            model_name='missionperson',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='missionsubmission',
            name='mission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='missions.mission', verbose_name='mission'),
        ),
        migrations.AlterField(
            model_name='missionsubmission',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mission_submissions', to='missions.missionperson', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='missionvisualization',
            name='mission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='missions.mission', verbose_name='mission'),
        ),
        migrations.AlterField(
            model_name='missionvisualization',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='missions.missionperson', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='missionvisualizationinstance',
            name='visualization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='missions.missionvisualization', verbose_name='visualization'),
        ),
    ]