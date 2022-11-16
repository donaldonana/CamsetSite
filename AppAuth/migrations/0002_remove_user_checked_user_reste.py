# Generated by Django 4.1.1 on 2022-11-16 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppComments', '0003_commentstats'),
        ('AppAuth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='checked',
        ),
        migrations.AddField(
            model_name='user',
            name='reste',
            field=models.ManyToManyField(related_name='reste', to='AppComments.comment'),
        ),
    ]
