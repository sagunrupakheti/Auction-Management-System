# Generated by Django 3.2.2 on 2021-05-29 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_app', '0009_remove_storebidding_estimated_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]
