# Generated by Django 5.0 on 2024-01-12 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DP_backend', '0002_remove_customuser_blood_group_customuser_activated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='activation_code',
            field=models.CharField(default='None'),
        ),
    ]
