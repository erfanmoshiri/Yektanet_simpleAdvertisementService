# Generated by Django 2.2.5 on 2021-10-10 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='Clicks',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='Image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='Views',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='advertiser',
            name='Clicks',
            field=models.IntegerField(null=True),
        ),
    ]