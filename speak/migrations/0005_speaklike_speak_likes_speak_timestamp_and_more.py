# Generated by Django 4.0.1 on 2022-01-18 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('speak', '0004_speak_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeakLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='speak',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='speak_user', through='speak.SpeakLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='speak',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='speaklike',
            name='speak',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='speak.speak'),
        ),
        migrations.AddField(
            model_name='speaklike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]