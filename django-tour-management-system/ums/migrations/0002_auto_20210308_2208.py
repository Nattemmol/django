# Generated by Django 3.1.3 on 2021-03-08 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0002_auto_20210308_2208'),
        ('ums', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='tour.destination'),
        ),
    ]
