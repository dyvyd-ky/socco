# Generated by Django 4.1.3 on 2022-12-23 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0005_lnmonline_delete_paymenttransaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lnmonline',
            name='Amount',
        ),
        migrations.RemoveField(
            model_name='lnmonline',
            name='Balance',
        ),
        migrations.RemoveField(
            model_name='lnmonline',
            name='MpesaReceiptNumber',
        ),
        migrations.RemoveField(
            model_name='lnmonline',
            name='PhoneNumber',
        ),
        migrations.RemoveField(
            model_name='lnmonline',
            name='TransactionDate',
        ),
        migrations.AddField(
            model_name='lnmonline',
            name='metadata',
            field=models.JSONField(default=dict),
        ),
    ]
