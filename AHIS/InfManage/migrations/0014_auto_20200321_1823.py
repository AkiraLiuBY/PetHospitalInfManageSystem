# Generated by Django 2.2.8 on 2020-03-21 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InfManage', '0013_auto_20200321_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseinf',
            name='PetCardID',
            field=models.CharField(max_length=12),
        ),
    ]