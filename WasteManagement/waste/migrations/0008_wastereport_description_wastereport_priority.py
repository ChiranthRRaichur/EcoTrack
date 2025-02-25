# Generated by Django 5.1.3 on 2024-11-29 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0007_remove_wastereport_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wastereport',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastereport',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=10),
        ),
    ]
