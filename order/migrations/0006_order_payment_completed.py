# Generated by Django 4.2 on 2025-03-08 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_remove_order_transactionid_order_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_completed',
            field=models.BooleanField(default=True),
        ),
    ]
