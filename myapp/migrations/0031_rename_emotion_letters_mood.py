# Generated by Django 5.1.6 on 2025-05-07 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_letters_detailed_mood_alter_letterroutine_emotion_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='letters',
            old_name='emotion',
            new_name='mood',
        ),
    ]
