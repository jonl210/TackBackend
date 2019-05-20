# Generated by Django 2.1.7 on 2019-05-20 00:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
        ('users', '0005_auto_20190319_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('u_id', models.CharField(default=0, max_length=11)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by', to='users.Profile')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='groups.Group')),
            ],
        ),
    ]
