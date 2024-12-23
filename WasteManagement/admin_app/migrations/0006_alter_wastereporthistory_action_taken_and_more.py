# Generated by Django 5.1.3 on 2024-12-15 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0005_alter_wastereportapproval_report_and_more'),
        ('waste', '0010_alter_wastereport_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wastereporthistory',
            name='action_taken',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Rejected', 'Rejected')], max_length=50),
        ),
        migrations.AlterField(
            model_name='wastereporthistory',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waste.wastereport'),
        ),
    ]
