# Generated by Django 2.2.4 on 2021-02-02 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_bigbluebutton', '0015_auto_20201214_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetinglog',
            name='meeting_id',
        ),
        migrations.AddField(
            model_name='meetinglog',
            name='meeting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='logs', to='django_bigbluebutton.Meeting', verbose_name='Meeting'),
        ),
        migrations.CreateModel(
            name='MeetingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.CharField(max_length=255, unique=True, verbose_name='Record ID')),
                ('meeting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='records', to='django_bigbluebutton.Meeting', verbose_name='Meeting')),
            ],
            options={
                'verbose_name': 'Meeting Record',
                'verbose_name_plural': 'Meeting Record',
                'db_table': 'meeting_record',
            },
        ),
    ]