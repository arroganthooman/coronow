# Generated by Django 3.1.2 on 2020-12-19 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidblog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='acc',
            field=models.BooleanField(default=False),
        ),
    ]
