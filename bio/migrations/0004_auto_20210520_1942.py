# Generated by Django 3.2.2 on 2021-05-20 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio', '0003_customuser_pronoums'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='pronoums',
            new_name='pronouns',
        ),
        migrations.AddField(
            model_name='customuser',
            name='description',
            field=models.TextField(default='', verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='pronouns',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='pronouns'),
        )
    ]
