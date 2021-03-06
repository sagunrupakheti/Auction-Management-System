# Generated by Django 3.2.2 on 2021-05-18 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auction_app', '0002_auto_20210517_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bidding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimated_price', models.IntegerField()),
                ('old_bid', models.IntegerField()),
                ('current_bid', models.IntegerField()),
                ('bidding_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='image1',
            field=models.ImageField(blank=True, upload_to='item_pics'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image2',
            field=models.ImageField(blank=True, upload_to='item_pics'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image3',
            field=models.ImageField(blank=True, upload_to='item_pics'),
        ),
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sold_price', models.IntegerField()),
                ('commission_amount', models.CharField(max_length=255)),
                ('payment_status', models.CharField(max_length=255)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='auction_app.bidding')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bidding',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='auction_app.item'),
        ),
    ]
