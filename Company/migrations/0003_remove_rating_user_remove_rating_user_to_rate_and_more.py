# Generated by Django 4.2.1 on 2023-05-21 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Company', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user_to_rate',
        ),
        migrations.AddField(
            model_name='rating',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='provider', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='stakeholder',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='stakeholder', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
