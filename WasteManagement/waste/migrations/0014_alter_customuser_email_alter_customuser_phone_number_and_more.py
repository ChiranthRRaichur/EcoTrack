# Generated by Django 5.1.3 on 2024-12-20 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0013_alter_customuser_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='points',
            field=models.IntegerField(default=0, verbose_name='Points'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='contact_information',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Contact Information'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='location',
            field=models.CharField(max_length=255, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='nearby_landmarks',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nearby Landmarks'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='photo',
            field=models.ImageField(upload_to='waste_photos/', verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='photo_hash',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Photo Hash'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=10, verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='wastereport',
            name='waste_type',
            field=models.CharField(max_length=50, verbose_name='Waste Type'),
        ),
    ]