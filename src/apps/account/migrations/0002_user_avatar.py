# Generated by Django 4.2.7 on 2024-05-06 14:25

import apps.account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=apps.account.models.get_upload_path),
        ),
    ]