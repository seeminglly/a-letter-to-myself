# Generated by Django 5.1.6 on 2025-04-04 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_alter_letterroutine_user_alter_letters_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letters',
            name='mood',
        ),
    ]
