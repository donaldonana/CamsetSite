# Generated by Django 4.1.1 on 2022-11-16 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppComments', '0002_comment_totaux_votes'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nbr_comment', models.IntegerField(default=4)),
                ('nbr_categorie', models.IntegerField(default=7221)),
            ],
        ),
    ]