# Generated by Django 5.0.2 on 2024-02-17 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='pyment_status',
            new_name='payment_status',
        ),
    ]