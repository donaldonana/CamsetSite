# Generated by Django 4.1.1 on 2022-10-29 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppComments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='totaux_votes',
            field=models.IntegerField(default=0),
        ),
    ]
