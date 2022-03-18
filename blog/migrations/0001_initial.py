# Generated by Django 4.0.2 on 2022-02-28 23:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, null=True, unique=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, null=True, unique=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, null=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='blog/images')),
                ('post_text', models.TextField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category')),
                ('tag', models.ManyToManyField(blank=True, to='blog.Tag')),
            ],
        ),
    ]
