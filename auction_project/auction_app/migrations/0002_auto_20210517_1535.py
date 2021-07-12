# Generated by Django 3.2 on 2021-05-17 09:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auction_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image1',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
        migrations.AddField(
            model_name='item',
            name='image2',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
        migrations.AddField(
            model_name='item',
            name='image3',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='item',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]