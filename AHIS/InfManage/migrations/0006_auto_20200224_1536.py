# Generated by Django 2.2.8 on 2020-02-24 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InfManage', '0005_auto_20200222_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseInf',
            fields=[
                ('CaseID', models.CharField(max_length=11, primary_key=True, serialize=False, unique=True)),
                ('PetOwnerName', models.CharField(max_length=20)),
                ('PetOwnerSex', models.CharField(max_length=2)),
                ('Tel', models.CharField(max_length=11)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('PostCode', models.CharField(max_length=6)),
                ('Address', models.CharField(max_length=30)),
                ('PetName', models.CharField(max_length=20)),
                ('Breed', models.CharField(max_length=20)),
                ('PetSex', models.CharField(max_length=2)),
                ('PetAge', models.IntegerField()),
                ('PetWeigth', models.FloatField()),
                ('Immune', models.CharField(max_length=30)),
                ('Sterilization', models.CharField(max_length=30)),
                ('PetCardID', models.CharField(max_length=11)),
                ('DoctorID', models.CharField(max_length=11)),
                ('Treatment', models.TextField(default='none')),
                ('Prescription', models.TextField(default='none')),
                ('TotalSum', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='managerinf',
            name='Email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
