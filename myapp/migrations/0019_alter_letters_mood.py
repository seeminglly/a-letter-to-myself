# Generated by Django 5.1.6 on 2025-03-17 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_letters_open_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letters',
            name='mood',
            field=models.CharField(choices=[('happy', '😊 행복'), ('sad', '😢 슬픔'), ('angry', '😡 화남'), ('worried', '🤔 고민')], default='happy', max_length=10),
        ),
    ]
