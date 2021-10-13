# Generated by Django 2.2.5 on 2021-10-11 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0003_auto_20211010_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AdId', models.CharField(max_length=40)),
                ('IpAddress', models.CharField(max_length=30)),
                ('CreatedAt', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AdId', models.CharField(max_length=40)),
                ('IpAddress', models.CharField(max_length=30)),
                ('CreatedAt', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='ad',
            name='Clicks',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='Views',
        ),
        migrations.RemoveField(
            model_name='advertiser',
            name='Clicks',
        ),
        migrations.RemoveField(
            model_name='advertiser',
            name='Views',
        ),
    ]