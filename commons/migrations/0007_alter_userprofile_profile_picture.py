# Generated by Django 5.1.6 on 2025-04-06 11:58

import commons.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0006_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='static/images/basicprofile.png', upload_to=commons.models.profile_picture_upload_to),
        ),
    ]
