# Generated by Django 4.2 on 2025-03-08 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0002_alter_mpesatransaction_checkout_request_id_and_more'),
        ('order', '0007_order_lipa_mdogo_order_outstanding_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='order.order')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mpesa.mpesatransaction')),
            ],
        ),
    ]
