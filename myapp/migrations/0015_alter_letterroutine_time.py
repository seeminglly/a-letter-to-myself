# Generated by Django 5.1.6 on 2025-03-14 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_letterroutine_routine_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letterroutine',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
