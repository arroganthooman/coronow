# Generated by Django 3.1.2 on 2020-11-18 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidstats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kasusprovinsi',
            name='str_update_terakhir',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='kasusupdated',
            name='str_update_terakhir',
            field=models.CharField(default='', max_length=100),
        ),
    ]