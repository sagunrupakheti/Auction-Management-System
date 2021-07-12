# Generated by Django 3.2.2 on 2021-05-31 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_app', '0012_item_item_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('notification_text', models.CharField(max_length=255)),
                ('concerned_to', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='item_name',
            field=models.CharField(max_length=255),
        ),
    ]
