# Generated by Django 5.1.1 on 2024-09-14 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0003_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='store_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
