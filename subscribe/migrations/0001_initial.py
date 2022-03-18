# Generated by Django 4.0.2 on 2022-03-08 05:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
            ],
        ),
    ]
