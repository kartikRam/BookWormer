# Generated by Django 5.0 on 2024-01-07 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('0', 'Out for Delivery'), ('1', 'Delivered')], default='0', max_length=50),
        ),
    ]
