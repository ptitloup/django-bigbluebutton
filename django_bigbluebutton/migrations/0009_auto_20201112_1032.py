# Generated by Django 2.2.5 on 2020-11-12 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_bigbluebutton', '0008_auto_20201008_1609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'verbose_name': 'Meeting', 'verbose_name_plural': 'Meeting'},
        ),
        migrations.AlterModelTable(
            name='meeting',
            table='meeting',
        ),
    ]