# Generated by Django 2.2.8 on 2020-04-14 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InfManage', '0020_auto_20200414_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorinf',
            name='Photo',
            field=models.ImageField(default='None', upload_to='media/'),
        ),
    ]