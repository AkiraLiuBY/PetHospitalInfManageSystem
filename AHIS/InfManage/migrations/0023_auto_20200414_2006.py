# Generated by Django 2.2.8 on 2020-04-14 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('InfManage', '0022_auto_20200414_1618'),
    ]

    operations = [
        migrations.RenameField(
            model_name='druginf',
            old_name='DurgToxicology',
            new_name='DrugToxicology',
        ),
    ]
