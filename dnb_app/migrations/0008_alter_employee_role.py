# Generated by Django 5.1.4 on 2025-06-09 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnb_app', '0007_alter_employee_phone_alter_employee_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('SUPER', 'Superuser'), ('ADMIN', 'Admin'), ('FIN', 'Finance Manager'), ('HR', 'HR Manager'), ('EMP', 'Employee')], default='EMP', help_text='System access level', max_length=15),
        ),
    ]
