# Generated by Django 4.2.1 on 2023-05-20 23:24

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(default='Company', max_length=100)),
                ('logo', models.ImageField(blank=True, upload_to='logo/')),
                ('tva', models.CharField(max_length=20)),
                ('emailToContact', models.EmailField(blank=True, max_length=254, null=True)),
                ('telephone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=30)),
                ('postcode', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('L', 'Luxembourg'), ('F', 'France'), ('BE', 'Belgique'), ('DE', 'Allemagne')], max_length=2)),
                ('interests', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None)),
                ('description', models.CharField(max_length=10000)),
                ('isAllowed', models.BooleanField(default=False)),
                ('darkMode', models.BooleanField(default=True)),
                ('newMember', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.CharField(max_length=1000)),
            ],
        ),
    ]
