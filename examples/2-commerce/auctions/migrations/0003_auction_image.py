# Generated by Django 3.1.5 on 2021-01-27 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210126_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='image',
            field=models.ImageField(null=True, upload_to='auctions/images'),
        ),
    ]