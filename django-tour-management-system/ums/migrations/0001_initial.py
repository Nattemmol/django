# Generated by Django 3.1.3 on 2021-02-21 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('country', models.CharField(choices=[('Nepal', 'Nepal'), ('Japan', 'Japan'), ('China', 'China'), ('India', 'India'), ('USA', 'USA'), ('Germany', 'Germany'), ('Thailand', 'Thailand')], max_length=200, null=True)),
                ('destination', models.CharField(choices=[('Langtang', 'Langtang'), ('Annapurna Circuit', 'Annapurna Circuit'), ('Everest Base Camp', 'Everest Base Camp'), ('Ghorepani Poon Hill', 'Ghorepani Poon Hill'), ('Upper Mustang', 'Upper Mustang')], max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
