# Generated by Django 2.2.8 on 2020-04-14 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InfManage', '0017_auto_20200414_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorinf',
            name='Photo',
            field=models.ImageField(default='None', upload_to='media/media/'),
        ),
    ]
