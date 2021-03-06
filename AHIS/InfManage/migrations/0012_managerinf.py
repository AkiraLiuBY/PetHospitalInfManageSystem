# Generated by Django 2.2.8 on 2020-03-15 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InfManage', '0011_delete_managerinf'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerInf',
            fields=[
                ('ManagerID', models.CharField(max_length=9, primary_key=True, serialize=False, unique=True)),
                ('PassWord', models.CharField(max_length=20)),
                ('ManagerName', models.CharField(max_length=20)),
                ('ManagerSex', models.CharField(max_length=2)),
                ('Tel', models.CharField(max_length=11)),
                ('Email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
