# Generated by Django 2.1.7 on 2019-03-12 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friendrequests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='from_user_username',
            field=models.CharField(default='placeholder', max_length=30),
        ),
    ]
