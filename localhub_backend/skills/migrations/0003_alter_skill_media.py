# Generated by Django 5.2.1 on 2025-06-05 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0002_alter_skill_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='media/cvs/'),
        ),
    ]
