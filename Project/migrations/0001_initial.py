# Generated by Django 4.2.1 on 2023-05-20 23:24

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('budget', models.FloatField()),
                ('description', models.TextField()),
                ('categoryL1', models.CharField(choices=[('IT', 'Informations & Technology'), ('S', 'Financial & Insurrance')], default='IT', max_length=2)),
                ('categoryL2', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=list, size=None)),
                ('status', models.CharField(choices=[('Y', 'Open'), ('B', 'In Progress'), ('C', 'Canceled'), ('G', 'Done')], default='Y', max_length=1)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('deadline_date', models.DateField(default=django.utils.timezone.now)),
                ('engaged_date', models.DateField(default=django.utils.timezone.now)),
                ('chatID', models.CharField()),
                ('file', models.FileField(blank=True, upload_to='tasks/')),
                ('archive', models.BooleanField(default=False)),
                ('pr_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_task', to=settings.AUTH_USER_MODEL)),
                ('pr_stakeholder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_task', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]