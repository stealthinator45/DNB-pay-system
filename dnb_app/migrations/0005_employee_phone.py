# Generated by Django 5.1.4 on 2025-06-07 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnb_app', '0004_department_alter_employee_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
