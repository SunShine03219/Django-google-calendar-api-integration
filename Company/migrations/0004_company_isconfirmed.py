# Generated by Django 4.2.1 on 2023-07-13 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0003_remove_rating_user_remove_rating_user_to_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='isConfirmed',
            field=models.BooleanField(default=False),
        ),
    ]
