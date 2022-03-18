# Generated by Django 4.0.2 on 2022-03-08 09:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('message', models.TextField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
            ],
        ),
    ]
