# Generated by Django 5.2.1 on 2025-06-05 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='cv',
            field=models.FileField(upload_to='media/cvs/'),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='media/logos/'),
        ),
    ]
