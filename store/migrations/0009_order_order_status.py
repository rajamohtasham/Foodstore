# Generated by Django 5.1.7 on 2025-03-25 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Received', 'Received'), ('Packed', 'Packed'), ('Dispatch', 'Dispatch'), ('Delivered', 'Delivered')], default='Received', max_length=10),
        ),
    ]
