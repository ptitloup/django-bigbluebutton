# Generated by Django 2.2.5 on 2020-11-26 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_bigbluebutton', '0009_auto_20201112_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='auto_start_recording',
            field=models.BooleanField(default=False, verbose_name='Auto Start Recording'),
        ),
    ]
