# Generated by Django 4.2 on 2025-02-16 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_amount_remove_order_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transactionID',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
