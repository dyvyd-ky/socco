# Generated by Django 4.1.3 on 2022-12-22 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0004_paymenttransaction_delete_lnmonline'),
    ]

    operations = [
        migrations.CreateModel(
            name='LNMOnline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CheckoutRequestID', models.CharField(blank=True, max_length=50, null=True)),
                ('MerchantRequestID', models.CharField(blank=True, max_length=20, null=True)),
                ('ResultCode', models.IntegerField(blank=True, null=True)),
                ('ResultDesc', models.CharField(blank=True, max_length=120, null=True)),
                ('Amount', models.FloatField(blank=True, null=True)),
                ('MpesaReceiptNumber', models.CharField(blank=True, max_length=15, null=True)),
                ('Balance', models.CharField(blank=True, max_length=12, null=True)),
                ('TransactionDate', models.DateTimeField(blank=True, null=True)),
                ('PhoneNumber', models.CharField(blank=True, max_length=13, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='PaymentTransaction',
        ),
    ]
