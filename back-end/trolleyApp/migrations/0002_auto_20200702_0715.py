# Generated by Django 2.2.14 on 2020-07-02 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trolleyApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.BigIntegerField(),
        ),
    ]
