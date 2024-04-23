# Generated by Django 4.2.10 on 2024-03-19 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('face_deviation', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('logins', models.IntegerField(default=0)),
                ('logouts', models.IntegerField(default=0)),
                ('copy_paste_attempt', models.BooleanField(default=False)),
                ('page_minimized', models.BooleanField(default=False)),
                ('user_inactivity_detected', models.BooleanField(default=False)),
                ('multiple_face_detected', models.BooleanField(default=False)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
