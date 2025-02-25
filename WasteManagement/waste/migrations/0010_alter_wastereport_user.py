# Generated by Django 5.1.3 on 2024-12-15 17:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0009_wastereport_latitude_wastereport_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wastereport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waste_reports', to=settings.AUTH_USER_MODEL),
        ),
    ]
